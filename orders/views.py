import logging
from datetime import date, timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from catalog.models import Package, package_for_due_date
from catalog.pricing import has_extras, single_price, subscription_price

from . import stripe_service
from .models import CustomerRequest, Order

log = logging.getLogger(__name__)


def _parse_date(value):
    try:
        return date.fromisoformat(value) if value else None
    except ValueError:
        return None


def checkout(request, slug):
    package = get_object_or_404(Package, slug=slug, is_active=True)
    plan = request.POST.get('plan') or request.GET.get('plan') or Order.PLAN_SUBSCRIPTION
    if plan not in (Order.PLAN_SUBSCRIPTION, Order.PLAN_SINGLE):
        plan = Order.PLAN_SUBSCRIPTION
    errors = {}
    form = {
        'due_date': request.POST.get('due_date') or request.GET.get('due_date') or request.session.get('due_date', ''),
        'birth_date': request.POST.get('birth_date', ''),
        'email': request.POST.get('email', ''),
        'accept_terms': bool(request.POST.get('accept_terms')),
        'consent_health': bool(request.POST.get('consent_health')),
        'skip_calcium': bool(request.POST.get('skip_calcium')),
        'extras': (request.POST.get('extras') or request.GET.get('extras') or '1') == '1',
        'marketing': bool(request.POST.get('marketing')),
    }

    if request.method == 'POST':
        due_date = _parse_date(form['due_date'])
        birth_date = _parse_date(form['birth_date'])
        if package.stage == Package.STAGE_PREGNANT:
            if not due_date:
                errors['due_date'] = 'Angiv din terminsdato, så vi kan sende den rigtige boks hver måned.'
            else:
                matched, _week = package_for_due_date(due_date)
                if due_date > date.today() + timedelta(days=290):
                    errors['due_date'] = 'Terminsdatoen ligger mere end 41 uger ude i fremtiden – tjek venligst året.'
                elif due_date < date.today() - timedelta(days=14):
                    errors['due_date'] = 'Terminsdatoen er passeret. Se vores pakke til tiden efter fødslen.'
                elif matched and matched.pk != package.pk and plan == Order.PLAN_SUBSCRIPTION:
                    # Start the subscription on the box that actually matches the due date.
                    messages.info(request, f'Ud fra din terminsdato starter dit abonnement med {matched.label} ({matched.weeks_label}).')
                    package = matched
        if (due_date or birth_date) and not form['consent_health']:
            errors['consent_health'] = 'Vi skal have dit samtykke for at gemme datoen.'
        if not form['accept_terms']:
            errors['accept_terms'] = 'Du skal acceptere handelsbetingelserne.'

        if not errors:
            extras = form['extras'] and has_extras(package)
            sub_price = subscription_price(package.stage, extras)
            order = Order.objects.create(
                plan=plan,
                start_package=package,
                due_date=due_date if package.stage == Package.STAGE_PREGNANT else None,
                birth_date=birth_date,
                amount=sub_price if plan == Order.PLAN_SUBSCRIPTION else single_price(package, extras),
                include_extras=extras,
                email=form['email'].strip(),
                marketing_consent=form['marketing'],
                skip_calcium=form['skip_calcium'],
            )
            if due_date:
                request.session['due_date'] = due_date.isoformat()
            if not settings.STRIPE_ENABLED:
                order.status = 'demo'
                order.save(update_fields=['status'])
                return redirect('checkout_demo', reference=order.reference)
            try:
                return redirect(stripe_service.create_checkout_session(order), permanent=False)
            except Exception:  # noqa: BLE001 – show a friendly error, log the details
                log.exception('Kunne ikke oprette Stripe Checkout for %s', order.reference)
                messages.error(request, 'Betalingen kunne ikke startes lige nu. Prøv igen om lidt, eller skriv til os.')

    return render(request, 'orders/checkout.html', {
        'package': package,
        'plan': plan,
        'sub_price': subscription_price(package.stage, form['extras']),
        'single_price': single_price(package, form['extras']),
        'has_extras': has_extras(package),
        'extras_names': sorted({c.item.nutrient for c in package.contents.select_related('item') if c.item.kind == 'supplement' and not c.sst_core}),
        'price_komplet': subscription_price(package.stage, True),
        'price_basis': subscription_price(package.stage, False),
        'form': form,
        'errors': errors,
    })


def checkout_success(request):
    session_id = request.GET.get('session_id', '')
    order = None
    if session_id and settings.STRIPE_ENABLED:
        try:
            order = stripe_service.apply_completed_session(stripe_service.retrieve_session(session_id))
        except Exception:  # noqa: BLE001
            log.exception('Kunne ikke hente Stripe session %s', session_id)
            order = Order.objects.filter(stripe_session_id=session_id).first()
    if order is None:
        return redirect('home')
    return render(request, 'orders/success.html', {'order': order, 'demo': False})


def checkout_demo(request, reference):
    order = get_object_or_404(Order, reference=reference, status='demo')
    return render(request, 'orders/success.html', {'order': order, 'demo': True})


def checkout_cancel(request, reference):
    order = get_object_or_404(Order, reference=reference)
    return render(request, 'orders/cancel.html', {'order': order})


@csrf_exempt
@require_POST
def stripe_webhook(request):
    if not settings.STRIPE_WEBHOOK_SECRET:
        return HttpResponseBadRequest('Webhook secret mangler')
    try:
        event = stripe_service.construct_event(request.body, request.META.get('HTTP_STRIPE_SIGNATURE', ''))
    except Exception:  # noqa: BLE001 – invalid payload or signature
        log.warning('Ugyldigt Stripe webhook-kald')
        return HttpResponseBadRequest('Invalid')
    stripe_service.handle_event(event)
    return HttpResponse(status=200)


def _receipt(req: CustomerRequest):
    """E-mail receipt to the customer (legal requirement for the withdrawal function) + copy to us."""
    what = 'fortrydelse' if req.kind == 'withdrawal' else 'opsigelse af abonnement'
    body = (
        f'Hej {req.name or ""}\n\n'
        f'Vi bekræfter, at vi {timezone.localtime(req.created_at):%d.%m.%Y kl. %H:%M} har modtaget din {what}.\n\n'
        f'Ordrenummer: {req.reference or "-"}\n'
        f'E-mail: {req.email}\n'
        + (f'Detaljer: {req.details}\n' if req.details else '')
        + (f'\n{req.result}\n' if req.result else '')
        + f'\nHar du spørgsmål, så svar på denne mail.\n\nVenlig hilsen\n{settings.COMPANY["legal_name"]}\n'
    )
    send_mail(f'Kvittering: {what} ({req.reference or "Motherbox"})', body, settings.DEFAULT_FROM_EMAIL,
              [req.email], fail_silently=True)
    send_mail(f'[Motherbox] Ny {what}: {req.reference}', body, settings.DEFAULT_FROM_EMAIL,
              [settings.COMPANY['email']], fail_silently=True)


def _find_order(reference, email):
    return Order.objects.filter(reference__iexact=reference.strip(), email__iexact=email.strip()).first()


def _two_step(request, kind, template):
    """Shared flow: fill in → review → 'Bekræft …' → receipt. Mirrors the statutory withdrawal-button flow."""
    data = {k: request.POST.get(k, '').strip() for k in ('reference', 'email', 'name', 'details')}
    step = request.POST.get('step', 'form') if request.method == 'POST' else 'form'
    errors = {}
    if step in ('review', 'confirm'):
        if '@' not in data['email']:
            errors['email'] = 'Angiv den e-mail, du bestilte med.'
        if kind == 'cancellation' and not data['reference']:
            errors['reference'] = 'Angiv dit ordrenummer (står i din ordrebekræftelse, fx MB1A2B3C4D).'
        if errors:
            step = 'form'
    if step == 'confirm':
        order = _find_order(data['reference'], data['email']) if data['reference'] else None
        req = CustomerRequest.objects.create(kind=kind, order=order, **data)
        if kind == 'cancellation':
            if order and order.stripe_subscription_id and settings.STRIPE_ENABLED:
                try:
                    stripe_service.cancel_subscription_at_period_end(order.stripe_subscription_id)
                    req.result = 'Abonnementet er opsagt og fornyes ikke igen. Allerede betalte bokse sendes som aftalt.'
                    req.handled = True
                except Exception:  # noqa: BLE001
                    log.exception('Kunne ikke opsige %s i Stripe', order.stripe_subscription_id)
                    req.result = 'Vi har registreret din opsigelse og bekræfter, når den er gennemført (senest næste hverdag).'
            else:
                req.result = 'Vi har registreret din opsigelse og bekræfter, når den er gennemført (senest næste hverdag).'
            req.save()
        _receipt(req)
        return render(request, 'orders/request_done.html', {'req': req})
    return render(request, template, {'data': data, 'step': step, 'errors': errors})


def withdraw(request):
    return _two_step(request, 'withdrawal', 'orders/withdraw.html')


def manage_subscription(request):
    return _two_step(request, 'cancellation', 'orders/manage.html')
