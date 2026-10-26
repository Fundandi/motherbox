import re
from datetime import date
from decimal import Decimal

from django.db import models
from django.templatetags.static import static
from django.urls import reverse


class Manufacturer(models.Model):
    """The company that actually makes a product. Shown publicly so customers can see exactly where every pill comes from."""
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    country = models.CharField(max_length=80)
    city = models.CharField(max_length=80, blank=True)
    founded = models.PositiveIntegerField(null=True, blank=True)
    website = models.URLField(blank=True)
    about = models.TextField(blank=True, help_text='Kort, faktuel beskrivelse af producenten.')
    production = models.TextField(blank=True, help_text='Hvor og hvordan der produceres (fx GMP-certificering), kun verificerede oplysninger.')
    review_platform = models.CharField(max_length=60, blank=True, help_text='Fx Trustpilot')
    review_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    review_count = models.PositiveIntegerField(null=True, blank=True)
    review_url = models.URLField(blank=True)
    review_checked = models.DateField(null=True, blank=True, help_text='Dato hvor anmeldelsestallet senest blev tjekket')
    b2b_contact = models.CharField(max_length=300, blank=True, help_text='Internt: hvordan vi køber ind en gros (vises ikke på siden)')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('manufacturer_detail', args=[self.slug])


class Item(models.Model):
    """A concrete retail product (original sealed pack) that goes into one or more boxes."""
    KIND_SUPPLEMENT = 'supplement'
    KIND_GOODIE = 'goodie'
    KIND_CHOICES = [(KIND_SUPPLEMENT, 'Kosttilskud'), (KIND_GOODIE, 'Goodie')]

    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default=KIND_SUPPLEMENT)
    name = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, related_name='items')
    nutrient = models.CharField(max_length=80, blank=True, help_text='Fx "Folsyre" – bruges til farve/ikon og gruppering')
    active_form = models.CharField(max_length=160, blank=True, help_text='Fx "Ferrobisglycinat (Ferrochel®)"')
    dose_per_unit = models.CharField(max_length=300, blank=True, help_text='Fx "400 µg pr. tablet" – eller "Folsyre 500 µg · Jern 39 mg · …" for en dagspose')
    unit_type = models.CharField(max_length=40, blank=True, help_text='tablet, kapsel, softgel, breve, g …')
    pack_size = models.CharField(max_length=60, blank=True, help_text='Fx "60 tabletter" eller "100 g"')
    units_per_pack = models.PositiveIntegerField(null=True, blank=True, help_text='Antal doseringsenheder i pakningen (bruges til refill-beregning)')
    description = models.TextField(blank=True)
    pregnancy_note = models.CharField(max_length=300, blank=True, help_text='Advarsel/bemærkning fra etiketten')
    label_info = models.TextField(blank=True, help_text='Obligatorisk mærkning (ingredienser, allergener, næringsindhold, anbefalet dosis, advarsler, nettoindhold, ansvarlig virksomhed) – skal vises før køb')

    # Where we buy it (purchasing list)
    retailer = models.CharField(max_length=80, blank=True)
    retailer_url = models.URLField(blank=True, max_length=500)
    alt_retailer = models.CharField(max_length=80, blank=True)
    alt_retailer_url = models.URLField(blank=True, max_length=500)
    retail_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text='Udsalgspris inkl. moms (DKK)')
    price_checked = models.DateField(null=True, blank=True)

    # Product-level reviews (from a named, public source)
    review_platform = models.CharField(max_length=60, blank=True)
    review_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    review_count = models.PositiveIntegerField(null=True, blank=True)
    review_url = models.URLField(blank=True, max_length=500)

    product_url = models.URLField(blank=True, max_length=500, help_text='Producentens egen produktside')
    verified = models.BooleanField(default=False, help_text='Alle oplysninger er tjekket mod en kilde')

    class Meta:
        ordering = ['kind', 'nutrient', 'name']

    def __str__(self):
        return f'{self.name} ({self.manufacturer})'

    SST_NUTRIENTS = ('folsyre', 'folat', 'd-vitamin', 'd3-vitamin', 'jern', 'calcium')

    @property
    def nutrient_lines(self):
        """Split dose_per_unit ("Folsyre 500 µg · Jern 39 mg · …") into rows for the box contents table."""
        rows = []
        for part in (self.dose_per_unit or '').split(' · '):
            part = part.strip()
            if not part:
                continue
            m = re.match(r'^(.*?)\s+([≥~]?\d.*)$', part)
            name, amount = (m.group(1), m.group(2)) if m else (part, '')
            rows.append({'name': name, 'amount': amount, 'sst': name.lower().startswith(self.SST_NUTRIENTS)})
        return rows


class Package(models.Model):
    STAGE_TTC = 'ttc'
    STAGE_PREGNANT = 'pregnant'
    STAGE_POSTPARTUM = 'postpartum'
    STAGE_CHOICES = [
        (STAGE_TTC, 'Ønsker at blive gravid'),
        (STAGE_PREGNANT, 'Gravid'),
        (STAGE_POSTPARTUM, 'Efter fødslen'),
    ]

    slug = models.SlugField(unique=True)
    position = models.PositiveSmallIntegerField(unique=True, help_text='Rækkefølge 0–10')
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)
    month = models.PositiveSmallIntegerField(null=True, blank=True, help_text='Graviditetsmåned (2–10), kun for gravid-pakker')
    week_start = models.PositiveSmallIntegerField(null=True, blank=True)
    week_end = models.PositiveSmallIntegerField(null=True, blank=True)
    title = models.CharField(max_length=120, help_text='Fx "Kvalme & kerne"')
    tagline = models.CharField(max_length=200, help_text='Én linje om hvad der sker i kroppen')
    body_now = models.TextField(help_text='Hvad sker der i denne periode')
    why = models.TextField(help_text='Hvorfor netop disse næringsstoffer')
    hero_nutrient = models.CharField(max_length=80, blank=True)
    image_url = models.URLField(blank=True, max_length=500)
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text='Pris for enkeltkøb (DKK inkl. moms)')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f'{self.label} – {self.title}'

    def get_absolute_url(self):
        return reverse('package_detail', args=[self.slug])

    @property
    def label(self):
        if self.stage == self.STAGE_PREGNANT:
            return 'Early Care' if (self.week_start or 0) < 10 else 'Late Care'
        if self.stage == self.STAGE_POSTPARTUM:
            return 'After Care'
        return 'Klar til graviditet'

    _IMAGES = {'klar-til-graviditet': 'klar', 'early-care': 'early', 'late-care': 'late', 'ammeboks': 'amme'}

    @property
    def stage_image(self):
        key = self._IMAGES.get(self.slug)
        return static(f'images/motherbox/stage-{key}.jpg') if key else self.image_url

    @property
    def box_image(self):
        """Main product photo: the box with two daily sachets on a kitchen table (AI-generated illustration)."""
        key = self._IMAGES.get(self.slug)
        return static(f'images/motherbox/side-{key}.jpg') if key else self.image_url

    @property
    def kit_image(self):
        """Close-up of the box with a hand holding one daily sachet (AI-generated illustration)."""
        key = self._IMAGES.get(self.slug)
        return static(f'images/motherbox/kit-{key}.jpg') if key else ''

    @property
    def pills_image(self):
        key = self._IMAGES.get(self.slug)
        return static(f'images/motherbox/pills-{key}.jpg') if key else ''

    @property
    def weeks_label(self):
        if self.week_start and self.week_end:
            return f'Uge {self.week_start}–{self.week_end}'
        if self.stage == self.STAGE_TTC:
            return 'Før graviditet'
        return '0–6 måneder efter fødslen'

    @property
    def supplements(self):
        return self.contents.filter(item__kind=Item.KIND_SUPPLEMENT).select_related('item__manufacturer')

    @property
    def goodies(self):
        return self.contents.filter(item__kind=Item.KIND_GOODIE).select_related('item__manufacturer')

    def cost_price(self):
        """Estimated purchase cost at retail prices (for internal margin calculations)."""
        total = Decimal('0')
        for c in self.contents.select_related('item'):
            if c.item.retail_price:
                total += c.item.retail_price * c.cost_share
        return total.quantize(Decimal('0.01'))


class PackageItem(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='contents')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='in_packages')
    daily_dose = models.CharField(max_length=120, blank=True, help_text='Anbefalet dosis i denne måned, fx "1 tablet (400 µg)"')
    short_dose = models.CharField(max_length=30, blank=True, help_text='Kort dosis til oversigtstabellen, fx "40 mg"')
    units_per_day = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('1'), help_text='Antal enheder pr. dag (til refill-beregning). 0 for goodies.')
    purpose = models.CharField(max_length=300, blank=True, help_text='Hvorfor det er med – kun godkendte/neutrale formuleringer')
    sst_core = models.BooleanField(default=False, help_text='Del af Sundhedsstyrelsens kerneanbefaling for denne periode')
    cost_share = models.DecimalField(
        max_digits=4, decimal_places=2, default=Decimal('1.00'),
        help_text='Andel af én pakning denne boks bruger (fx 0,5 hvis pakningen dækker 2 bokse)',
    )
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['position', 'id']

    def __str__(self):
        return f'{self.package.label}: {self.item.name}'


def package_for_due_date(due_date, today=None):
    """Return the Package matching a due date: pregnancy week ≥ 41 → postpartum, otherwise the month box covering the week."""
    today = today or date.today()
    week = 40 - (due_date - today).days / 7
    if week > 40.5:
        return Package.objects.filter(stage=Package.STAGE_POSTPARTUM, is_active=True).first(), week
    week_int = min(40, max(5, int(week) + 1))  # "uge 5" = 4+0 to 4+6; anyone earlier starts on the first pregnancy box
    pkg = Package.objects.filter(
        stage=Package.STAGE_PREGNANT, is_active=True, week_start__lte=week_int, week_end__gte=week_int
    ).first()
    return pkg, week


class Advisor(models.Model):
    """'Hvem spørger vi til råds' on the front page. Shown by profession, not by person, and only for advisers we actually work with.
    Health professionals must not appear to recommend the products (EU 1924/2006 art. 12(c)), so the text describes what they advise on."""
    role = models.CharField(max_length=80, help_text='Fx "Jordemoder" – vises som overskrift')
    slug = models.SlugField(unique=True)
    advises_on = models.CharField(max_length=300, help_text='Hvad vi spørger dem om. Ikke "anbefaler", ikke produktudtalelser.')
    name = models.CharField(max_length=120, blank=True, help_text='Internt – vises ikke på siden')
    position = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['position', 'role']
        verbose_name = 'rådgiver'
        verbose_name_plural = 'rådgivere'

    def __str__(self):
        return self.role
