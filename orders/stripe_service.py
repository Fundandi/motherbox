"""Thin wrapper around Stripe Checkout + webhook handling."""
import logging
from datetime import datetime, timezone as dt_timezone
from decimal import Decimal

import stripe
from django.conf import settings
from django.urls import reverse

from .models import Order, StripeEvent

log = logging.getLogger(__name__)


def client():
    return stripe.StripeClient(settings.STRIPE_SECRET_KEY)


def _ore(amount: Decimal) -> int:
    return int((amount * 100).quantize(Decimal('1')))


def create_checkout_session(order: Order) -> str:
    """Create a Stripe Checkout Session for the order and return its URL."""
    pkg = order.start_package
    success = settings.SITE_URL + reverse('checkout_success') + '?session_id={CHECKOUT_SESSION_ID}'
    cancel = settings.SITE_URL + reverse('checkout_cancel', args=[order.reference])
    metadata = {'order_reference': order.reference, 'start_package': pkg.slug}

    if order.plan == Order.PLAN_SUBSCRIPTION:
        line_item = {
            'quantity': 1,
            'price_data': {
                'currency': 'dkk',
                'unit_amount': _ore(order.amount),
                'recurring': {'interval': 'month'},
                'product_data': {
                    'name': 'Motherbox abonnement',
                    'description': f'Månedlig boks tilpasset din fase. Første boks: {pkg.label}. '
                                   'Fri fragt. Opsig når som helst.',
                },
            },
        }
    else:
        line_item = {
            'quantity': 1,
            'price_data': {
                'currency': 'dkk',
                'unit_amount': _ore(order.amount),
                'product_data': {
                    'name': f'Motherbox {pkg.label}',
                    'description': 'Enkelt boks. Fri fragt.',
                },
            },
        }

    params = {
        'mode': 'subscription' if order.plan == Order.PLAN_SUBSCRIPTION else 'payment',
        'line_items': [line_item],
        'success_url': success,
        'cancel_url': cancel,
        'client_reference_id': order.reference,
        'metadata': metadata,
        'locale': 'da',
        'allow_promotion_codes': True,
        'billing_address_collection': 'auto',
        'shipping_address_collection': {'allowed_countries': ['DK']},
        'phone_number_collection': {'enabled': True},
    }
    if settings.STRIPE_PAYMENT_METHOD_TYPES:
        params['payment_method_types'] = settings.STRIPE_PAYMENT_METHOD_TYPES
    if order.email:
        params['customer_email'] = order.email
    if order.plan == Order.PLAN_SUBSCRIPTION:
        params['subscription_data'] = {'metadata': metadata}
    else:
        params['customer_creation'] = 'always'
        params['payment_intent_data'] = {'metadata': metadata}
        params['invoice_creation'] = {'enabled': True}

    session = client().v1.checkout.sessions.create(params=params)
    order.stripe_session_id = session.id
    order.save(update_fields=['stripe_session_id', 'updated_at'])
    return session.url


def retrieve_session(session_id: str):
    return client().v1.checkout.sessions.retrieve(session_id)


def apply_completed_session(session) -> Order | None:
    """Copy customer + shipping details from a completed Checkout Session onto our Order. Idempotent."""
    session = _as_dict(session)
    ref = session.get('client_reference_id') or (session.get('metadata') or {}).get('order_reference')
    order = Order.objects.filter(reference=ref).first() if ref else None
    if order is None:
        order = Order.objects.filter(stripe_session_id=session.get('id')).first()
    if order is None:
        log.warning('Stripe session %s matcher ingen ordre', session.get('id'))
        return None

    details = session.get('customer_details') or {}
    # Newer API versions put shipping under collected_information.shipping_details
    shipping = (session.get('collected_information') or {}).get('shipping_details') or session.get('shipping_details') or {}
    address = shipping.get('address') or details.get('address') or {}

    order.email = details.get('email') or order.email
    order.name = shipping.get('name') or details.get('name') or order.name
    order.phone = details.get('phone') or order.phone
    order.address_line1 = address.get('line1') or ''
    order.address_line2 = address.get('line2') or ''
    order.postal_code = address.get('postal_code') or ''
    order.city = address.get('city') or ''
    order.country = address.get('country') or 'DK'
    order.stripe_customer_id = session.get('customer') or order.stripe_customer_id
    sub = session.get('subscription')
    order.stripe_subscription_id = (sub if isinstance(sub, str) else (sub or {}).get('id')) or order.stripe_subscription_id
    if session.get('payment_status') in ('paid', 'no_payment_required') and order.status in ('pending', 'past_due'):
        order.status = 'paid'
    order.save()
    return order


def construct_event(payload: bytes, sig_header: str):
    return stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)


def handle_event(event) -> None:
    """Process one verified webhook event exactly once."""
    event = _as_dict(event)
    _, created = StripeEvent.objects.get_or_create(event_id=event['id'], defaults={'type': event['type']})
    if not created:
        return
    obj = event['data']['object']
    etype = event['type']

    if etype in ('checkout.session.completed', 'checkout.session.async_payment_succeeded'):
        apply_completed_session(obj)
    elif etype == 'checkout.session.async_payment_failed':
        Order.objects.filter(stripe_session_id=obj['id']).update(status='past_due')
    elif etype == 'invoice.paid':
        sub_id = _invoice_subscription_id(obj)
        if sub_id:
            Order.objects.filter(stripe_subscription_id=sub_id).exclude(status='cancelled').update(status='paid')
    elif etype == 'invoice.payment_failed':
        sub_id = _invoice_subscription_id(obj)
        if sub_id:
            Order.objects.filter(stripe_subscription_id=sub_id).update(status='past_due')
    elif etype == 'customer.subscription.deleted':
        Order.objects.filter(stripe_subscription_id=obj['id']).update(status='cancelled')
    elif etype == 'customer.subscription.updated':
        if obj.get('status') in ('canceled', 'unpaid', 'incomplete_expired'):
            Order.objects.filter(stripe_subscription_id=obj['id']).update(status='cancelled')
        elif obj.get('status') == 'past_due':
            Order.objects.filter(stripe_subscription_id=obj['id']).update(status='past_due')
        elif obj.get('status') == 'active':
            Order.objects.filter(stripe_subscription_id=obj['id']).update(status='paid')


def _invoice_subscription_id(invoice):
    # API ≥ 2025-03 moved it to parent.subscription_details.subscription
    sub = invoice.get('subscription')
    if not sub:
        sub = ((invoice.get('parent') or {}).get('subscription_details') or {}).get('subscription')
    return sub if isinstance(sub, str) else (sub or {}).get('id') if sub else None


def _as_dict(obj):
    return obj.to_dict() if hasattr(obj, 'to_dict') else obj


def cancel_subscription_at_period_end(subscription_id: str):
    """Stop future renewals; the customer keeps the box already paid for."""
    return client().v1.subscriptions.update(subscription_id, params={'cancel_at_period_end': True})
