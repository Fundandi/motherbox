from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from catalog import seed_data
from catalog.models import Advisor, Item, Manufacturer, Package, PackageItem


class Command(BaseCommand):
    help = 'Opretter producenter, produkter og pakkerne fra catalog/seed_data.py. Eksisterende rækker røres ikke uden --update.'

    def add_arguments(self, parser):
        parser.add_argument('--update', action='store_true', help='Overskriv eksisterende rækker med seed-data (inkl. pakkeindhold).')

    @transaction.atomic
    def handle(self, *args, update=False, **opts):
        def upsert(model, slug, data):
            obj = model.objects.filter(slug=slug).first()
            if obj is None:
                return model.objects.create(slug=slug, **data), True
            if update:
                for k, v in data.items():
                    setattr(obj, k, v)
                obj.save()
            return obj, False

        created = {'producenter': 0, 'produkter': 0, 'pakker': 0}
        makers = {}
        for m in seed_data.MANUFACTURERS:
            m = dict(m)
            slug = m.pop('slug')
            makers[slug], new = upsert(Manufacturer, slug, m)
            created['producenter'] += new

        items = {}
        for i in seed_data.ITEMS:
            i = dict(i)
            slug = i.pop('slug')
            i['manufacturer'] = makers[i.pop('manufacturer')]
            if i.get('retail_price') is not None:
                i['retail_price'] = Decimal(str(i['retail_price']))
            items[slug], new = upsert(Item, slug, i)
            created['produkter'] += new

        # Boxes that are no longer in the seed (e.g. the old 11-box structure) are retired: hidden and moved out of the way of
        # the unique position numbers. They are kept (not deleted) because existing orders may reference them.
        seed_slugs = {p['slug'] for p in seed_data.PACKAGES}
        for old in Package.objects.exclude(slug__in=seed_slugs).filter(position__lt=100):
            old.is_active = False
            old.position = 100 + old.pk
            old.save(update_fields=['is_active', 'position'])

        for p in seed_data.PACKAGES:
            p = dict(p)
            slug = p.pop('slug')
            contents = p.pop('contents')
            p['price'] = Decimal(str(p['price']))
            pkg, new = upsert(Package, slug, p)
            created['pakker'] += new
            if new or update:
                pkg.contents.all().delete()
                for pos, c in enumerate(contents):
                    PackageItem.objects.create(
                        package=pkg, item=items[c['item']], position=pos,
                        daily_dose=c.get('dose', ''), purpose=c.get('purpose', ''), short_dose=c.get('short', ''),
                        sst_core=c.get('sst', False), cost_share=Decimal(str(c.get('share', 1))),
                        units_per_day=Decimal(str(c.get('upd', 0 if items[c['item']].kind == Item.KIND_GOODIE else 1))),
                    )

        # Advisors are edited in admin, so the seed only creates missing rows and never overwrites them.
        for a in seed_data.ADVISORS:
            a = dict(a)
            Advisor.objects.get_or_create(slug=a.pop('slug'), defaults=a)

        self.stdout.write(self.style.SUCCESS(
            'Seed færdig: ' + ', '.join(f'{v} nye {k}' for k, v in created.items()) + (' (eksisterende opdateret)' if update else '')
        ))
