from datetime import date, timedelta
from decimal import Decimal
from unittest import mock

from django.test import TestCase, override_settings
from django.urls import reverse

from catalog.models import Item, Manufacturer, Package, PackageItem, package_for_due_date

from . import stripe_service
from .models import Order, StripeEvent


def make_catalog():
    m = Manufacturer.objects.create(name='Testproducent', slug='test', country='Danmark')
    item = Item.objects.create(name='Folsyre 400', slug='folsyre', manufacturer=m, nutrient='Folsyre')
    Package.objects.create(slug='ttc', position=0, stage='ttc', title='Klar', tagline='t', body_now='b', why='w', price=Decimal('349'))
    for i, month in enumerate(range(2, 11), start=1):
        p = Package.objects.create(
            slug=f'maaned-{month}', position=i, stage='pregnant', month=month,
            week_start=(month - 1) * 4 + 1, week_end=month * 4,
            title=f'M{month}', tagline='t', body_now='b', why='w', price=Decimal('449'),
        )
        PackageItem.objects.create(package=p, item=item, daily_dose='1 tablet', sst_core=True)
    Package.objects.create(slug='efter', position=10, stage='postpartum', title='Efter', tagline='t', body_now='b', why='w', price=Decimal('399'))


class PackageForDueDateTests(TestCase):
    def setUp(self):
        make_catalog()
        self.today = date(2026, 10, 1)

    def due_in_weeks(self, weeks_left):
        return self.today + timedelta(weeks=weeks_left)

    def test_week_boundaries(self):
        cases = {
            36: 'maaned-2',   # 4+0 → uge 5
            33: 'maaned-2',   # 7+0 → uge 8
            32: 'maaned-3',   # 8+0 → uge 9
            28: 'maaned-4',   # 12+0 → uge 13
            4: 'maaned-10',   # 36+0 → uge 37
            0: 'maaned-10',   # termin
        }
        for weeks_left, slug in cases.items():
            pkg, _ = package_for_due_date(self.due_in_weeks(weeks_left), today=self.today)
            self.assertEqual(pkg.slug, slug, f'{weeks_left} uger til termin')

    def test_very_early_starts_on_first_pregnancy_box(self):
        pkg, _ = package_for_due_date(self.due_in_weeks(39), today=self.today)
        self.assertEqual(pkg.slug, 'maaned-2')

    def test_after_due_date_is_postpartum(self):
        pkg, _ = package_for_due_date(self.today - timedelta(days=7), today=self.today)
        self.assertEqual(pkg.slug, 'efter')


@override_settings(STRIPE_SECRET_KEY='', STRIPE_ENABLED=False)
class DemoCheckoutTests(TestCase):
    def setUp(self):
        make_catalog()

    def test_pregnant_checkout_requires_due_date_and_terms(self):
        r = self.client.post(reverse('checkout', args=['maaned-4']), {'plan': 'subscription'})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'terminsdato')
        self.assertEqual(Order.objects.count(), 0)

    def test_subscription_starts_on_box_matching_due_date(self):
        due = date.today() + timedelta(weeks=20)  # uge 21 → måned 6
        r = self.client.post(reverse('checkout', args=['maaned-2']), {
            'plan': 'subscription', 'due_date': due.isoformat(), 'accept_terms': '1', 'consent_health': '1', 'email': 'a@b.dk',
        })
        order = Order.objects.get()
        self.assertRedirects(r, reverse('checkout_demo', args=[order.reference]))
        self.assertEqual(order.status, 'demo')
        self.assertEqual(order.start_package.slug, 'maaned-6')
        self.assertEqual(order.amount, Decimal('349'))

    def test_one_subscription_price_for_all_boxes(self):
        due = (date.today() + timedelta(weeks=20)).isoformat()
        for extras, price in (('1', '349'), ('0', '349')):
            self.client.post(reverse('checkout', args=['maaned-6']), {
                'plan': 'subscription', 'due_date': due, 'accept_terms': '1', 'consent_health': '1', 'extras': extras})
            self.assertEqual(Order.objects.latest('id').amount, Decimal(price))

    def test_due_date_requires_health_consent(self):
        due = date.today() + timedelta(weeks=20)
        r = self.client.post(reverse('checkout', args=['maaned-6']), {'plan': 'subscription', 'due_date': due.isoformat(), 'accept_terms': '1'})
        self.assertContains(r, 'samtykke')
        self.assertEqual(Order.objects.count(), 0)

    def test_single_box_uses_package_price(self):
        self.client.post(reverse('checkout', args=['ttc']), {'plan': 'single', 'accept_terms': '1'})
        order = Order.objects.get()
        self.assertEqual(order.plan, 'single')
        self.assertEqual(order.amount, Decimal('349'))

    def test_pages_render(self):
        for name, args in [('home', []), ('package_list', []), ('package_detail', ['maaned-5']),
                           ('manufacturer_list', []), ('manufacturer_detail', ['test']), ('science', []),
                           ('about', []), ('faq', []), ('terms', []), ('privacy', []), ('withdrawal', []),
                           ('checkout', ['maaned-5'])]:
            r = self.client.get(reverse(name, args=args))
            self.assertEqual(r.status_code, 200, name)


@override_settings(STRIPE_SECRET_KEY='sk_test_x', STRIPE_ENABLED=True, STRIPE_WEBHOOK_SECRET='whsec_x')
class StripeFlowTests(TestCase):
    def setUp(self):
        make_catalog()

    def test_checkout_redirects_to_stripe(self):
        fake = mock.Mock(id='cs_test_1', url='https://checkout.stripe.com/c/pay/cs_test_1')
        with mock.patch.object(stripe_service, 'client') as client:
            client.return_value.v1.checkout.sessions.create.return_value = fake
            r = self.client.post(reverse('checkout', args=['ttc']), {'plan': 'subscription', 'accept_terms': '1'})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r['Location'], fake.url)
        params = client.return_value.v1.checkout.sessions.create.call_args.kwargs['params']
        self.assertEqual(params['mode'], 'subscription')
        self.assertEqual(params['line_items'][0]['price_data']['unit_amount'], 34900)  # one price for all boxes
        self.assertEqual(params['line_items'][0]['price_data']['recurring'], {'interval': 'month'})
        self.assertEqual(Order.objects.get().stripe_session_id, 'cs_test_1')

    def _event(self, etype, obj, eid='evt_1'):
        return {'id': eid, 'type': etype, 'data': {'object': obj}}

    def test_webhook_lifecycle(self):
        order = Order.objects.create(plan='subscription', start_package=Package.objects.get(slug='ttc'), amount=Decimal('399'))
        session = {
            'id': 'cs_1', 'client_reference_id': order.reference, 'payment_status': 'paid',
            'customer': 'cus_1', 'subscription': 'sub_1',
            'customer_details': {'email': 'kunde@test.dk', 'name': 'Kunde', 'phone': '+4512345678', 'address': None},
            'collected_information': {'shipping_details': {'name': 'Kunde Hansen', 'address': {
                'line1': 'Testvej 1', 'line2': None, 'postal_code': '8000', 'city': 'Aarhus', 'country': 'DK'}}},
        }
        stripe_service.handle_event(self._event('checkout.session.completed', session))
        order.refresh_from_db()
        self.assertEqual((order.status, order.email, order.city, order.stripe_subscription_id), ('paid', 'kunde@test.dk', 'Aarhus', 'sub_1'))
        self.assertEqual(order.name, 'Kunde Hansen')

        # Duplicate delivery is ignored
        stripe_service.handle_event(self._event('checkout.session.completed', session))
        self.assertEqual(StripeEvent.objects.count(), 1)

        stripe_service.handle_event(self._event('invoice.payment_failed', {'parent': {'subscription_details': {'subscription': 'sub_1'}}}, 'evt_2'))
        order.refresh_from_db()
        self.assertEqual(order.status, 'past_due')

        stripe_service.handle_event(self._event('invoice.paid', {'subscription': 'sub_1'}, 'evt_3'))
        order.refresh_from_db()
        self.assertEqual(order.status, 'paid')

        stripe_service.handle_event(self._event('customer.subscription.deleted', {'id': 'sub_1'}, 'evt_4'))
        order.refresh_from_db()
        self.assertEqual(order.status, 'cancelled')

    def test_webhook_rejects_bad_signature(self):
        r = self.client.post(reverse('stripe_webhook'), data=b'{}', content_type='application/json', HTTP_STRIPE_SIGNATURE='bad')
        self.assertEqual(r.status_code, 400)


class FulfilmentTests(TestCase):
    def setUp(self):
        make_catalog()
        m = Manufacturer.objects.get()
        self.folsyre = Item.objects.get(slug='folsyre')
        self.folsyre.units_per_pack = 90
        self.folsyre.save()
        self.tea = Item.objects.create(name='Rooibos', slug='rooibos', kind='goodie', manufacturer=m)
        for p in Package.objects.filter(stage='pregnant'):
            PackageItem.objects.create(package=p, item=self.tea, units_per_day=0)

    def test_refill_only_when_running_out(self):
        from .fulfilment import simulate
        start = date(2026, 1, 1)
        order = Order(plan='subscription', start_package=Package.objects.get(slug='maaned-2'),
                      due_date=start + timedelta(weeks=36), amount=Decimal('399'))
        boxes = simulate(order, start, 4)
        folsyre_per_box = [sum(ln.quantity for ln in lines if ln.item == self.folsyre) for _, _, lines in boxes]
        # 90 tablets at 1/day: shipped in box 1, again when <37 days left (box 3), not in between
        self.assertEqual(folsyre_per_box, [1, 0, 1, 0])
        # goodie in every box
        self.assertTrue(all(any(ln.item == self.tea for ln in lines) for _, _, lines in boxes))

    def test_skip_calcium(self):
        from .fulfilment import box_contents
        m = Manufacturer.objects.get()
        ca = Item.objects.create(name='Calcium 500', slug='ca', manufacturer=m, nutrient='Calcium', units_per_pack=60)
        pkg = Package.objects.get(slug='maaned-5')
        PackageItem.objects.create(package=pkg, item=ca, units_per_day=2)
        order = Order(plan='subscription', start_package=pkg, amount=Decimal('449'))
        self.assertIn(ca, [ln.item for ln in box_contents(order, date(2026, 1, 1), ledger={})])
        order.skip_calcium = True
        self.assertNotIn(ca, [ln.item for ln in box_contents(order, date(2026, 1, 1), ledger={})])

    def test_goodies_rotate_with_pregnancy_week(self):
        from .fulfilment import box_contents
        m = Manufacturer.objects.get()
        late = Package.objects.create(slug='late', position=20, stage='pregnant', week_start=10, week_end=40,
                                      title='Late Care', tagline='t', body_now='b', why='w', price=Decimal('349'), is_active=False)
        cookies = Item.objects.create(name='Kiks', slug='kiks', kind='goodie', manufacturer=m)
        pads = Item.objects.create(name='Ammeindlæg', slug='pads', kind='goodie', manufacturer=m)
        PackageItem.objects.create(package=late, item=cookies, units_per_day=0, short_dose='10–13')
        PackageItem.objects.create(package=late, item=pads, units_per_day=0, short_dose='38–40')
        ship = date(2026, 1, 1)
        order = Order(plan='subscription', start_package=late, amount=Decimal('349'))
        order.package_for_shipment = lambda d: late
        order.due_date = ship + timedelta(weeks=29)  # uge 12
        self.assertEqual([ln.item for ln in box_contents(order, ship, ledger={})], [cookies])
        order.due_date = ship + timedelta(weeks=1)  # uge 40
        self.assertEqual([ln.item for ln in box_contents(order, ship, ledger={})], [pads])


class NutrientLinesTests(TestCase):
    def test_split_dose_per_unit(self):
        item = Item(dose_per_unit='Folsyre 500 µg · Jern 39 mg · DHA 500 mg · Probiotika')
        self.assertEqual(item.nutrient_lines, [
            {'name': 'Folsyre', 'amount': '500 µg', 'sst': True},
            {'name': 'Jern', 'amount': '39 mg', 'sst': True},
            {'name': 'DHA', 'amount': '500 mg', 'sst': False},
            {'name': 'Probiotika', 'amount': '', 'sst': False},
        ])


@override_settings(STRIPE_ENABLED=False, EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class CustomerRequestTests(TestCase):
    def setUp(self):
        make_catalog()

    def test_withdrawal_two_step_with_receipt(self):
        from django.core import mail
        from .models import CustomerRequest
        r = self.client.post(reverse('withdraw'), {'step': 'review', 'email': 'a@b.dk', 'reference': 'MB123'})
        self.assertContains(r, 'Bekræft fortrydelse')
        self.assertEqual(CustomerRequest.objects.count(), 0)
        r = self.client.post(reverse('withdraw'), {'step': 'confirm', 'email': 'a@b.dk', 'reference': 'MB123', 'name': 'A'})
        self.assertContains(r, 'modtaget')
        self.assertEqual(CustomerRequest.objects.get().kind, 'withdrawal')
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn('a@b.dk', mail.outbox[0].to)

    def test_cancellation_requires_reference(self):
        r = self.client.post(reverse('manage_subscription'), {'step': 'review', 'email': 'a@b.dk'})
        self.assertContains(r, 'ordrenummer')

    @override_settings(STRIPE_ENABLED=True, STRIPE_SECRET_KEY='sk_test_x')
    def test_cancellation_cancels_stripe_subscription(self):
        order = Order.objects.create(plan='subscription', start_package=Package.objects.get(slug='ttc'), amount=Decimal('199'),
                                     email='k@b.dk', stripe_subscription_id='sub_9', status='paid')
        with mock.patch.object(stripe_service, 'cancel_subscription_at_period_end') as cancel:
            self.client.post(reverse('manage_subscription'), {'step': 'confirm', 'email': 'K@B.dk', 'reference': order.reference.lower()})
        cancel.assert_called_once_with('sub_9')
