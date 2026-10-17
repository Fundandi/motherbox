"""Write the purchasing list (Indkøbsliste.md) straight from the catalogue, so it always matches the boxes.

    python manage.py purchase_list            # → ../Indkøbsliste.md
"""
from datetime import date
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from catalog.models import Item, Manufacturer, Package
from orders.fulfilment import box_contents
from orders.models import Order


def kr(v):
    return f'{Decimal(v):,.2f} kr'.replace(',', 'X').replace('.', ',').replace('X', '.') if v is not None else '—'


class Command(BaseCommand):
    help = 'Skriver Indkøbsliste.md ud fra kataloget.'

    def add_arguments(self, parser):
        parser.add_argument('--out', default=str(Path(settings.BASE_DIR).parent / 'Indkøbsliste.md'))

    def handle(self, *args, out, **opts):
        L = []
        w = L.append
        w('# Motherbox – Indkøbsliste')
        w('')
        w(f'Genereret {date.today():%d.%m.%Y} fra produktkataloget (`python manage.py purchase_list`). Priserne er udsalgspriser inkl. moms, som de stod hos forhandleren 30.09.2026. **Tjek pris og lager, før du bestiller.** Helsam havde flere varer i restordre.')
        w('')
        w('**Sådan bruges listen**')
        w('- **Før CVR og engrosaftaler:** køb i detail via linkene i "Hvor køber jeg".')
        w('- **Når CVR og Fødevarestyrelsen-registrering er på plads:** kontakt leverandørerne i kolonnen "Engros". Målet er mindst 30–40 % under udsalgspris, og det er forudsat i prisen (se Enhedsøkonomi).')
        w('- **Hver måned:** Admin → Ordrer → *Pakkeliste denne måned* viser præcis, hvad der skal købes til de aktive kunder. Den regner med refill, så fulde pakninger kun sendes, når kunden er ved at løbe tør.')
        w('')

        # ── Products ──
        for kind, title in ((Item.KIND_SUPPLEMENT, 'Kosttilskud'), (Item.KIND_GOODIE, 'Goodies')):
            w(f'## {title}')
            w('')
            w('| Produkt | Producent | Pakning | Pris | Hvor køber jeg | Alternativ | Bruges i |')
            w('|---|---|---|---|---|---|---|')
            for i in Item.objects.filter(kind=kind).select_related('manufacturer').prefetch_related('in_packages__package').order_by('nutrient', 'name'):
                boxes = ', '.join(sorted({pi.package.label for pi in i.in_packages.all()}, key=lambda x: (len(x), x)))
                main = f'[{i.retailer}]({i.retailer_url})' if i.retailer_url else '—'
                alt = f'[{i.alt_retailer}]({i.alt_retailer_url})' if i.alt_retailer_url else '—'
                w(f'| **{i.name}**<br><small>{i.dose_per_unit}</small> | {i.manufacturer.name} | {i.pack_size} | {kr(i.retail_price)} | {main} | {alt} | {boxes} |')
            w('')

        # ── Wholesale contacts ──
        w('## Engros / leverandørkontakter')
        w('')
        w('| Producent | Sådan køber du en gros |')
        w('|---|---|')
        for m in Manufacturer.objects.exclude(b2b_contact='').order_by('name'):
            w(f'| {m.name} | {m.b2b_contact} |')
        w('')

        # ── Per box ──
        w('## Indhold pr. boks (første boks til en ny kunde)')
        w('')
        w('Første boks indeholder fulde pakninger. De følgende bokse genopfylder kun det, kunden er ved at løbe tør for (se `orders/fulfilment.py`). Tallene er "Komplet" inkl. calcium. "Basis" fjerner tillæg (DHA, magnesium).')
        w('')
        total_all = Decimal('0')
        for pkg in Package.objects.all():
            order = Order(plan=Order.PLAN_SUBSCRIPTION, start_package=pkg, amount=0)
            if pkg.stage == Package.STAGE_PREGNANT:
                # a due date that puts "today" in the middle of this box's weeks
                from datetime import timedelta
                mid = (pkg.week_start + pkg.week_end) / 2
                order.due_date = date.today() + timedelta(weeks=40 - mid + 0.5)
            lines = box_contents(order, date.today(), ledger={})
            cost = sum((ln.item.retail_price or 0) * ln.quantity for ln in lines)
            total_all += cost
            w(f'### {pkg.label} · {pkg.weeks_label} — {pkg.title}')
            w('')
            w('| Antal | Produkt | Daglig dosis | Hvor |')
            w('|---|---|---|---|')
            doses = {c.item_id: c.daily_dose for c in pkg.contents.all()}
            for ln in lines:
                where = f'[{ln.item.retailer}]({ln.item.retailer_url})' if ln.item.retailer_url else '—'
                w(f'| {ln.quantity} | {ln.item.name} ({ln.item.pack_size}) | {doses.get(ln.item.pk) or "—"} | {where} |')
            w('')
            w(f'Udsalgspris for indholdet: **{kr(cost)}**')
            w('')

        w('## Prøvesæt')
        w('')
        w(f'Køb én første boks af hver af de 11 pakker til fotos, test og til diætistens gennemgang: ca. **{kr(total_all)}** i detail. Mange produkter går igen, så køber du hvert produkt én gang, er beløbet markant lavere. Se "Engangsindkøb" nedenfor.')
        w('')
        uniq = sum((i.retail_price or 0) for i in Item.objects.all())
        w('## Engangsindkøb: ét eksemplar af hvert produkt')
        w('')
        w(f'{Item.objects.count()} produkter, i alt ca. **{kr(uniq)}** i detail.')
        w('')

        w('## Emballage og fragt')
        w('')
        w('| Hvad | Hvor | Pris (ekskl. moms) |')
        w('|---|---|---|')
        w('| Brevsprækkeæske / postæske | [Rajapack](https://www.rajapack.dk) | fra 3,45 kr./stk. (brevsprække) · fra 2,15 kr. (postæske) |')
        w('| Fragt, pakkeshop | [Shipmondo](https://www.shipmondo.com) (gratis konto) → GLS | ca. 34,80 kr. |')
        w('| Fragt, pakkeshop | Shipmondo → dao | ca. 38,43 kr. |')
        w('| Fragt, levering til døren | Shipmondo → dao HOME | ca. 42,51 kr. |')
        w('| Indlægsseddel (dosering pr. måned + "tag ikke flere produkter med samme næringsstof") | Egen print | ca. 1 kr. |')
        w('')
        w('_Priserne på emballage og fragt kommer fra `research/jura_og_drift.md`._')
        Path(out).write_text('\n'.join(L), encoding='utf-8')
        self.stdout.write(self.style.SUCCESS(f'Skrev {out}'))
