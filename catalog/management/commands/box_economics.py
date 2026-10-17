"""Simulate subscribers through the programme and print purchase cost per box vs. revenue.

    python manage.py box_economics --wholesale-discount 0.30 --shipping 45 --packaging 12
"""
from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand

from catalog.models import Item, Package
from catalog.pricing import subscription_price
from orders.fulfilment import simulate
from orders.models import Order

VAT = Decimal('1.25')


class Command(BaseCommand):
    help = 'Enhedsøkonomi pr. boks (refill-logik) for typiske kundeforløb.'

    def add_arguments(self, parser):
        parser.add_argument('--wholesale-discount', type=float, default=0.30, help='Rabat ift. udsalgspris ved grossistkøb (0.30 = 30 %%)')
        parser.add_argument('--shipping', type=float, default=45, help='Fragt pr. boks ekskl. moms')
        parser.add_argument('--packaging', type=float, default=12, help='Emballage + indlægsseddel pr. boks ekskl. moms')
        parser.add_argument('--stripe-pct', type=float, default=0.025, help='Betalingsgebyr i %% af beløb inkl. moms (Stripe EU-kort ca. 1,5 %% + 1,80 kr)')

    def handle(self, *args, **o):
        disc = Decimal(str(o['wholesale_discount']))
        ship = Decimal(str(o['shipping']))
        pack = Decimal(str(o['packaging']))
        fee_pct = Decimal(str(o['stripe_pct']))

        start = date(2026, 1, 5)
        journeys = {
            'Gravid fra uge 5 (måned 2) → 3 mdr. efter fødslen': (Package.objects.get(slug='maaned-2'), start + timedelta(weeks=36), 12),
            'Gravid fra uge 13 (måned 4) → 3 mdr. efter fødslen': (Package.objects.get(slug='maaned-4'), start + timedelta(weeks=28), 10),
            'Klar til graviditet i 3 mdr.': (Package.objects.get(slug='klar-til-graviditet'), None, 3),
        }
        for title, (pkg, due, months) in journeys.items():
            order = Order(plan=Order.PLAN_SUBSCRIPTION, start_package=pkg, due_date=due, amount=subscription_price(pkg.stage))
            self.stdout.write(self.style.MIGRATE_HEADING(f'\n{title}'))
            self.stdout.write(f'{"Dato":<12}{"Boks":<24}{"Indhold":<60}{"Indkøb ex moms":>16}{"Dækningsbidrag":>16}')
            tot_rev = tot_cost = Decimal('0')
            for d, box, lines in simulate(order, start, months):
                price = subscription_price(box.stage if box else None)
                net = price / VAT
                goods = sum((ln.item.retail_price or 0) * ln.quantity for ln in lines) / VAT * (1 - disc)
                cost = goods + ship + pack + price * fee_pct
                tot_rev += net
                tot_cost += cost
                content = ', '.join(f'{ln.quantity}×{ln.item.name.split()[0 if ln.item.kind == Item.KIND_GOODIE else -1][:14]}' for ln in lines)
                self.stdout.write(f'{d:%d.%m.%y}  {box.label if box else "-":<24}{content[:58]:<60}{goods:>13.0f} kr{net - cost:>13.0f} kr')
            margin = (tot_rev - tot_cost) / tot_rev * 100 if tot_rev else 0
            self.stdout.write(self.style.SUCCESS(
                f'Omsætning ex moms {tot_rev:.0f} kr · omkostninger {tot_cost:.0f} kr · dækningsbidrag {tot_rev - tot_cost:.0f} kr ({margin:.0f} %) · pr. md. {(tot_rev - tot_cost) / months:.0f} kr'))
