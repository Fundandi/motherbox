"""Catalogue seed data for Motherbox. Goodie prices/URLs checked 2026-09-30, JemoPharm/Zentabox data 2026-10-12/17 (see ../research/*.json).

Reviews: only figures we could see on a named public page are included. Brand-level Trustpilot scores with very few
reviews are shown as-is (with their count) rather than hidden — transparency over polish.
"""
from datetime import date

from .seed_labels import LABEL_SOURCES, LABELS
from .seed_packages import PACKAGE_TEXTS

CHECKED = date(2026, 9, 30)

MANUFACTURERS = [
    # ── Kosttilskud ──
    {
        'slug': 'jemopharm', 'name': 'JemoPharm', 'country': 'Danmark', 'city': 'Stege, Møn', 'founded': 1986,
        'website': 'https://jemopharm.dk',
        'about': 'JemoPharm A/S (CVR 10216109), Hasselvej 1, 4780 Stege, er en dansk virksomhed, der siden 1986 har udviklet naturbaserede lægemidler, '
                 'naturlægemidler og kosttilskud. JemoPharm står bl.a. bag VitaCare®, der sælges på danske apoteker og i helsekostbutikker, og bag abonnementsmærket Zentabox. '
                 'JemoPharm er en del af The Whole Company A/S. Motherbox forhandler Zentabox-dagsposer, som JemoPharm producerer, i original og uåbnet emballage.',
        'production': 'Produceres af JemoPharm på Møn. Zentabox A/S (Unionsvej 4, 4600 Køge, CVR 37447250) er ansvarlig virksomhed for mærkningen. Én original pakning med 30 forseglede dagsposer pr. boks.',
        'review_platform': 'Trustpilot (Zentabox, JemoPharms mærke)', 'review_rating': '4.7', 'review_count': 300,
        'review_url': 'https://dk.trustpilot.com/review/zentabox.dk', 'review_checked': date(2026, 10, 17),
    },
    # ── Goodies: to danske grossister ──
    {'slug': 'naturesource', 'name': 'NatureSource', 'country': 'Danmark', 'city': 'Vedbæk',
     'website': 'https://www.naturesource.dk',
     'about': 'NatureSource I/S, Vedbæk Stationsvej 37C, 2950 Vedbæk (lager i Ringsted), er dansk distributør af økologiske fødevarer. '
              'Vi køber disse mærker hos NatureSource: Clipper (te), Hampstead (te), Gin Gins (ingefærkarameller), Island Bakery (kiks) og Clearspring (græskarkerner).'},
    {'slug': 'biogan', 'name': 'Biogan', 'country': 'Danmark', 'city': 'Lystrup',
     'website': 'https://www.biogan.dk',
     'about': 'Biogan A/S, Møgelbakken 3-5, 8520 Lystrup, er en dansk grossist og eget mærke for økologiske fødevarer. '
              'Vi køber Biogans egne økologiske dadler og Panela ingefærpastiller hos Biogan.'},
]

S = 'supplement'
G = 'goodie'

ITEMS = [
    # ── Zentabox-dagsposer (produceret af JemoPharm), forhandlet i original emballage: 30 dagsposer pr. pakning (én pakning = én boks) ──
    {
        'slug': 'motherbox-klar', 'kind': S, 'manufacturer': 'jemopharm', 'name': 'Zentabox Baby Me',
        'nutrient': 'Folsyre', 'unit_type': 'dagspose', 'pack_size': '30 dagsposer', 'units_per_pack': 30,
        'dose_per_unit': 'Folsyre 400 µg · Zink',
        'description': 'Zentabox Baby Me til dig, der prøver at blive gravid: folsyre 400 µg, zink og Asparagus officinalis. Leveres i original Zentabox-pakning.',
        'label_info': 'Zentabox Baby Me – anbefalet daglig dosis 1 tablet: 400 µg folsyre, zink samt Asparagus officinalis.\n'
                      'Ansvarlig virksomhed: Zentabox A/S, Unionsvej 4, 4600 Køge (CVR 37447250).\nProduceret af JemoPharm A/S, Hasselvej 1, 4780 Stege.\nDen fulde varedeklaration står på den originale pakning.\nKilde: https://zentabox.dk/produkter',
        'product_url': 'https://zentabox.dk/produkter', 'verified': False,
    },
    {
        'slug': 'motherbox-early-care', 'kind': S, 'manufacturer': 'jemopharm', 'name': 'Zentabox Early Care',
        'nutrient': 'Multi', 'unit_type': 'dagspose', 'pack_size': '30 dagsposer', 'units_per_pack': 30,
        'dose_per_unit': 'Folsyre 400 µg · D-vitamin 10 µg',
        'description': 'Zentabox-dagspose til graviditetens første uger (til og med uge 9) med Sundhedsstyrelsens anbefalinger om folsyre og D-vitamin. Leveres i original Zentabox-pakning.',
        'label_info': 'Den endelige varedeklaration for Zentabox-pakningen til uge 5–9 modtages fra Zentabox før lancering. '
                      'Pakken er sammensat efter Sundhedsstyrelsens anbefalinger for graviditetens første uger: 400 µg folsyre og 10 µg D-vitamin dagligt.\n'
                      'Ansvarlig virksomhed: Zentabox A/S, Unionsvej 4, 4600 Køge (CVR 37447250).\nProduceret af JemoPharm A/S, Hasselvej 1, 4780 Stege.',
        'verified': False,
    },
    {
        'slug': 'motherbox-late-care', 'kind': S, 'manufacturer': 'jemopharm', 'name': 'Zentabox Pregnant Late Care',
        'nutrient': 'Multi', 'unit_type': 'dagspose', 'pack_size': '30 dagsposer', 'units_per_pack': 30,
        'dose_per_unit': 'Folsyre 500 µg · D3-vitamin 10 µg · Jern 39 mg · Jod 175 µg · Calcium 300 mg · Magnesium 160 mg · DHA 500 mg · EPA 148 mg · Vitamin A 400 µg · Probiotika',
        'active_form': 'Jern bl.a. som ferrobisglycinat',
        'description': 'Zentabox Pregnant Late Care: dagspose fra uge 10 til fødslen. Leveres i original Zentabox-pakning.',
        'pregnancy_note': 'Indeholder vitamin A (400 µg som retinylacetat). Tag ikke andre produkter med vitamin A eller jern samtidig uden at tale med din læge eller jordemoder.',
        'label_info': 'Næringsindhold pr. dagspose (ifølge Zentabox Pregnant Late Care, 30 doser): folsyre 500 µg, D3-vitamin 10 µg, jod 175 µg, jern 39 mg (14 mg + 25 mg ferrobisglycinat), '
                      'vitamin A 400 µg (retinylacetat), calcium 300 mg, magnesium 160 mg, DHA 500 mg, EPA 148 mg samt probiotika.\n'
                      'Anbefalet daglig dosis: 1 dagspose.\nAnsvarlig virksomhed: Zentabox A/S, Unionsvej 4, 4600 Køge (CVR 37447250).\nProduceret af JemoPharm A/S, Hasselvej 1, 4780 Stege.\n'
                      'Leveres i original, uåbnet Zentabox-pakning.\nKilde: https://www.webapoteket.dk/zentabox-pregnant-late-care-30-doser',
        'retail_price': 249, 'price_checked': date(2026, 10, 12), 'verified': False,
    },
    {
        'slug': 'motherbox-amme', 'kind': S, 'manufacturer': 'jemopharm', 'name': 'Zentabox Mommy Care After',
        'nutrient': 'Multi', 'unit_type': 'dagspose', 'pack_size': '30 dagsposer', 'units_per_pack': 30,
        'dose_per_unit': 'Folsyre 500 µg · D-vitamin 10 µg · Jern 15 mg · Jod 200 µg · Calcium 300 mg · Magnesium 160 mg · DHA 500 mg · Vitamin A 400 µg · Probiotika',
        'description': 'Zentabox Mommy Care After: dagspose til dig, der ammer. Leveres i original Zentabox-pakning.',
        'label_info': 'Næringsindhold pr. dagspose (ifølge Zentabox Mommy Care After, 30 doser): folsyre 500 µg, D-vitamin 10 µg, jod 200 µg, jern 15 mg, '
                      'vitamin A 400 µg (retinylacetat), calcium 300 mg, magnesium 160 mg, DHA 500 mg samt probiotika.\n'
                      'Anbefalet daglig dosis: 1 dagspose.\nAnsvarlig virksomhed: Zentabox A/S, Unionsvej 4, 4600 Køge (CVR 37447250).\nProduceret af JemoPharm A/S, Hasselvej 1, 4780 Stege.\n'
                      'Leveres i original, uåbnet Zentabox-pakning.\nKilde: https://www.webapoteket.dk/zentabox-mommy-care-after-30-doser',
        'retail_price': 249, 'price_checked': date(2026, 10, 12), 'verified': False,
    },
    # ── Goodies ──
    {'slug': 'clipper-rooibos', 'kind': G, 'manufacturer': 'naturesource', 'name': 'Clipper Rooibos Te Ø', 'nutrient': 'Urtete',
     'pack_size': '20 breve', 'retailer': 'Helsebixen', 'retailer_url': 'https://www.helsebixen.dk/shop/clipper-te-rooibos-20-breve.html',
     'alt_retailer': 'Matas', 'alt_retailer_url': 'https://www.matas.dk/clipper-rooibos-te-20-breve', 'retail_price': 21.00, 'price_checked': CHECKED,
     'pregnancy_note': 'Koffeinfri og uden lakrids. Fødevarestyrelsen anbefaler højst et par kopper te om dagen og at variere mellem mærker.', 'verified': True},
    {'slug': 'clipper-kamille', 'kind': G, 'manufacturer': 'naturesource', 'name': 'Clipper Kamille Te Ø', 'nutrient': 'Urtete',
     'pack_size': '20 breve', 'retailer': 'Helsam', 'retailer_url': 'https://helsam.dk/products/kamille-te-o-clipper',
     'alt_retailer': 'Matas', 'alt_retailer_url': 'https://www.matas.dk/clipper-kamille-te-20-breve', 'retail_price': 34.95, 'price_checked': CHECKED,
     'pregnancy_note': 'Højst et par kopper om dagen. Undlad ved allergi over for kurvblomster.', 'verified': True},
    {'slug': 'hampstead-citron-ingefaer', 'kind': G, 'manufacturer': 'naturesource', 'name': 'Hampstead Citron & Ingefær Te Ø (Demeter)', 'nutrient': 'Urtete',
     'pack_size': '20 breve', 'retailer': 'Helsam', 'retailer_url': 'https://www.helsam.dk/products/citron-ingefaer-te-o-demeter',
     'retail_price': 41.95, 'price_checked': CHECKED,
     'pregnancy_note': 'Uden lakridsrod, i modsætning til mange ingefærteer. Fødevarestyrelsen fraråder ingefærshots og -tilskud til gravide, men ikke ingefær i almindelige fødevarer.', 'verified': True},
    {'slug': 'gin-gins-original', 'kind': G, 'manufacturer': 'naturesource', 'name': 'Gin Gins Ginger Chews Original', 'nutrient': 'Snack',
     'pack_size': '42 g', 'retailer': 'Helsam', 'retailer_url': 'https://helsam.dk/products/ginger-chews-gin-gins-r-original-travel-pack',
     'retail_price': 30.95, 'price_checked': CHECKED, 'pregnancy_note': 'Ingefær i fødevaremængde. Indeholder soja.', 'verified': True},
    {'slug': 'panela-ingefaer-pastiller', 'kind': G, 'manufacturer': 'biogan', 'name': 'Panela Ingefær Pastiller Ø', 'nutrient': 'Snack',
     'pack_size': '30 g', 'retailer': 'Helsam', 'retailer_url': 'https://helsam.dk/products/ingefaer-pastiller-m-gurkemejesmag-o',
     'retail_price': 22.95, 'price_checked': CHECKED, 'verified': True},
    {'slug': 'island-bakery-oat-raisin', 'kind': G, 'manufacturer': 'naturesource', 'name': 'Island Bakery Oat & Raisin Cookies Ø', 'nutrient': 'Snack',
     'pack_size': '2 stk (30 g)', 'retailer': 'Helsam', 'retailer_url': 'https://helsam.dk/products/oat-raisin-cookies-2-pak-o',
     'retail_price': 16.95, 'price_checked': CHECKED, 'verified': True},
    {'slug': 'clearspring-tamari-graeskarkerner', 'kind': G, 'manufacturer': 'naturesource', 'name': 'Clearspring Tamari-ristede Græskarkerner Ø', 'nutrient': 'Kerner',
     'pack_size': '30 g', 'retailer': 'Helsam', 'retailer_url': 'https://helsam.dk/products/tamari-ristede-graeskarkerner-o',
     'retail_price': 14.95, 'price_checked': CHECKED, 'pregnancy_note': 'Indeholder soja.', 'verified': True},
    {'slug': 'biogan-dadler', 'kind': G, 'manufacturer': 'biogan', 'name': 'Biogan Dadler u. sten Ø', 'nutrient': 'Tørret frugt',
     'pack_size': '500 g', 'retailer': 'Helsam', 'retailer_url': 'https://www.helsam.dk/products/dadler-u-sten-o',
     'retail_price': 69.95, 'price_checked': CHECKED, 'verified': True},
]

# Contents per box. upd = units per day (refill calc). sst = part of Sundhedsstyrelsen's recommendation.
TTC_PACK = {'item': 'motherbox-klar', 'dose': '1 dagspose', 'short': 'Folsyre', 'sst': True,
            'purpose': 'Dækker Sundhedsstyrelsens anbefaling om 400 µg folsyre, fra du planlægger graviditet.'}
EARLY_PACK = {'item': 'motherbox-early-care', 'dose': '1 dagspose', 'short': 'Folsyre + D', 'sst': True,
              'purpose': 'Dækker Sundhedsstyrelsens anbefaling om folsyre (400 µg) og D-vitamin (10 µg) i graviditetens første uger.'}
LATE_PACK = {'item': 'motherbox-late-care', 'dose': '1 dagspose', 'short': 'Jern + D + DHA', 'sst': True,
             'purpose': 'Jern fra uge 10, D-vitamin og DHA i én daglig pose. Sundhedsstyrelsen anbefaler 40–50 mg jern fra uge 10 og 10 µg D-vitamin hele graviditeten.'}
AMME_PACK = {'item': 'motherbox-amme', 'dose': '1 dagspose', 'short': 'D + jod + DHA', 'sst': True,
             'purpose': 'Dækker Sundhedsstyrelsens anbefaling om 10 µg D-vitamin, mens du ammer, og indeholder også jod og DHA.'}


def goodie(slug, purpose='', weeks=''):
    """weeks = "10–13" means: only sent while the customer is in that pregnancy-week window (Late Care rotates goodies)."""
    return {'item': slug, 'purpose': purpose, 'upd': 0, 'short': weeks}


CONTENTS = {
    'klar-til-graviditet': [TTC_PACK,
                            goodie('clipper-rooibos', 'Koffeinfri te. Fødevarestyrelsen anbefaler at begrænse koffein, allerede når man prøver at blive gravid.'),
                            goodie('clearspring-tamari-graeskarkerner', 'Ristede græskarkerner i snackpose.')],
    'early-care': [EARLY_PACK,
                   goodie('gin-gins-original', 'Ingefærkarameller i almindelig fødevaremængde. Rart at have i tasken.'),
                   goodie('panela-ingefaer-pastiller', 'Små, milde ingefærpastiller.'),
                   goodie('hampstead-citron-ingefaer', 'Ingefærte uden lakrids.')],
    # Late Care: the supplement is the same every month; goodies follow the pregnancy week (4-week windows).
    'late-care': [LATE_PACK,
                  goodie('hampstead-citron-ingefaer', 'Ingefærte uden lakrids til de sidste kvalme-uger.', '10–13'),
                  goodie('island-bakery-oat-raisin', 'Tørre havrekiks, som mange har glæde af om morgenen.', '10–13'),
                  goodie('clipper-rooibos', 'Koffeinfri te.', '14–17'),
                  goodie('clearspring-tamari-graeskarkerner', 'Ristede græskarkerner i snackpose.', '14–17'),
                  goodie('clipper-kamille', 'Kamillete til aftenen.', '18–21'),
                  goodie('panela-ingefaer-pastiller', 'Små, milde ingefærpastiller til tasken.', '18–21'),
                  goodie('island-bakery-oat-raisin', 'Havrekiks til eftermiddagen.', '22–25'),
                  goodie('clipper-rooibos', 'Koffeinfri te.', '22–25'),
                  goodie('clearspring-tamari-graeskarkerner', 'Ristede græskarkerner i snackpose.', '26–29'),
                  goodie('hampstead-citron-ingefaer', 'Ingefærte uden lakrids.', '26–29'),
                  goodie('clipper-kamille', 'Til en rolig kop te om aftenen.', '30–33'),
                  goodie('island-bakery-oat-raisin', 'Havrekiks til eftermiddagen.', '30–33'),
                  goodie('biogan-dadler', 'Økologiske dadler. Mange spiser dadler i de sidste uger af graviditeten.', '34–37'),
                  goodie('clipper-rooibos', 'Koffeinfri te.', '34–37'),
                  goodie('biogan-dadler', 'Økologiske dadler til de sidste uger.', '38–40'),
                  goodie('island-bakery-oat-raisin', 'Noget sødt til hospitalstasken.', '38–40')],
    'ammeboks': [AMME_PACK,
                 goodie('clipper-kamille', 'Til en rolig kop te mellem amningerne.'),
                 goodie('island-bakery-oat-raisin', 'Noget sødt til amningen.')],
}

# 'Hvem spørger vi til råds' – kun rådgivere vi faktisk arbejder med. Oprettes kun første gang; ret og udvid derefter i admin.
ADVISORS = [
    {'slug': 'sygeplejerske', 'role': 'Sygeplejerske', 'name': 'Camilla Stær', 'position': 0,
     'advises_on': 'Hvordan boksene passer ind i hverdagen før, under og efter graviditeten – og hvad gravide spørger om.'},
    {'slug': 'ernaeringsekspert', 'role': 'Ernæringsekspert', 'name': 'Zentabox', 'position': 1,
     'advises_on': 'Indholdet af dagsposerne set i forhold til Sundhedsstyrelsens anbefalinger for hver fase.'},
]

SINGLE_PRICES = {}
DEFAULT_SINGLE_PRICE = 399

PACKAGES = [
    dict(p, price=SINGLE_PRICES.get(p['slug'], DEFAULT_SINGLE_PRICE), contents=CONTENTS[p['slug']])
    for p in PACKAGE_TEXTS
]

for _i in ITEMS:
    if _i['slug'] in LABELS:
        _i['label_info'] = LABELS[_i['slug']] + (f"\nKilde: {LABEL_SOURCES[_i['slug']]}" if LABEL_SOURCES.get(_i['slug']) else '')
