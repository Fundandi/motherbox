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
        'nutrient': 'Folsyre', 'unit_type': 'dagspose', 'pack_size': '30 dagsposer til hende + 30 til ham', 'units_per_pack': 30,
        # Her daily sachet (Baby Me + D3 + mælkesyrebakterier + øjentablet), summed per nutrient.
        'dose_per_unit': 'Folsyre 400 µg · D-vitamin 50 µg · Zink 20 mg · B6-vitamin 6,84 mg · B12-vitamin 12 µg · Riboflavin 1,4 mg · '
                         'C-vitamin 80 mg · Mælkesyrebakterier 5 mia. CFU · Lutein 4,3 mg · Lykopen 5,1 mg · Blåbærekstrakt 150 mg · '
                         'Asparagus officinalis 50 mg · Vitex agnus-castus 50 mg · Grøn te-ekstrakt 50 mg',
        'description': 'Dagspose til dig, der prøver at blive gravid: Baby Me (folsyre 400 µg, zink, D-, B6-, B12-vitamin og riboflavin), '
                       'D3-vitamin 40 µg, mælkesyrebakterier og en tablet med blåbær, lutein og lykopen. '
                       'Boksen har også en dagspose til din partner med D3-vitamin 40 µg, mælkesyrebakterier, zink 22 mg og selen 100 µg. '
                       'Leveres i original Zentabox-pakning.',
        'pregnancy_note': 'Baby Me indeholder grøn te-ekstrakt og kyskhedstræ (Vitex agnus-castus) og må ikke tages af gravide eller ammende. '
                          'Stop med Baby Me, så snart graviditetstesten er positiv – dit abonnement skifter da til Early Care. '
                          'Tag ikke andre kosttilskud med grøn te samme dag, og tag ikke tabletten på tom mave.',
        'label_info': 'HENDE – 1 dagspose:\n'
                      'Baby Me, 1 tablet: folsyre 400 µg (200 % RI), zink 15 mg (150 % RI), D-vitamin 10 µg (200 % RI), riboflavin 1,4 mg (100 % RI), '
                      'B6-vitamin 6 mg (429 % RI), B12-vitamin 12 µg (480 % RI), Asparagus officinalis 50 mg, Vitex agnus-castus 50 mg, grøn te-ekstrakt 50 mg. '
                      'Ingredienser: antiklumpningsmidler (dikalciumfosfat, siliciumdioxid), fyldemidler (mikrokrystallinsk cellulose, tværbundet natriumcarboxymethylcellulose, '
                      'magnesiumsalte af fedtsyrer), kyskhedstræekstrakt (Vitex agnus-castus L.), grøn te-ekstrakt (Camellia sinensis L. Kuntze), aspargesekstrakt (Asparagus officinalis L.), '
                      'zinkoxid, overfladebehandlingsmidler (hydroxypropylmethylcellulose, polyethylenglycol, ethylcellulose, hydroxypropylcellulose, glycerol, talkum), '
                      'pyridoxinhydroklorid, riboflavin, folsyre, farvestoffer (kaliumaluminiumsilikat, jernoxider og jernhydroxider), cyanocobalamin, cholecalciferol. '
                      'Grøn te-ekstrakt indeholder EGCG; højst 800 mg EGCG pr. dag. Må ikke indtages af gravide, ammende eller børn under 18 år.\n'
                      'D3-vitamin, 1 tablet: 40 µg (800 % RI). Ingredienser: fyldemidler (dikalciumfosfat, mikrokrystallinsk cellulose, magnesiumsalte af fedtsyrer), '
                      'overfladebehandlingsmidler (hydroxypropylmethylcellulose, talkum, polyethylenglycol, hydroxypropylcellulose, ethylcellulose, glycerol), '
                      'antiklumpningsmiddel (siliciumdioxid), antioxidant (DL-alfa-tocopherol), cholecalciferol, farvestof (riboflavin).\n'
                      'Mælkesyrebakterier, 1 kapsel: Bifidobacterium lactis Bl041 2,0 mia. CFU, Lactiplantibacillus plantarum Lp-141 1,7 mia., '
                      'Lactobacillus acidophilus La-121 300 mio., Lacticaseibacillus rhamnosus LR111 1 mia., B6-vitamin 0,84 mg (60 % RI). '
                      'Ingredienser: fruktooligosakkarider, kapselskal (hydroxypropylmethylcellulose), majsstivelse, fyldemiddel (mikrokrystallinsk cellulose), '
                      'mælkesyrebakterierne ovenfor, antiklumpningsmiddel (magnesiumsalte af fedtsyrer), pyridoxinhydrochlorid.\n'
                      'Blåbær, lutein og lykopen, 1 stk.: blåbær 150 mg, C-vitamin 80 mg, lutein 4,3 mg, lykopen 5,1 mg, zink 5 mg, anthocyanin 10 mg. '
                      'Ingredienser: blåbærekstrakt (Vaccinium myrtillus L.), anthocyanin, tagetesekstrakt (Tagetes erecta L.), lykopen, '
                      'kapselskal (hydroxypropylmethylcellulose), L-ascorbinsyre, zinkoxid, konsistensmiddel (magnesiumsalte af fedtsyrer).\n\n'
                      'HAM – 1 dagspose:\n'
                      'D3-vitamin, 1 tablet: 40 µg (800 % RI) – ingredienser som ovenfor.\n'
                      'Mælkesyrebakterier, 1 kapsel – som ovenfor.\n'
                      'Zink, 1 tablet: 22 mg (220 % RI). Ingredienser: fyldemidler (dikalciumfosfat, mikrokrystallinsk cellulose), zinkoxid, '
                      'antiklumpningsmidler (magnesiumsalte af fedtsyrer, siliciumdioxid).\n'
                      'Selen, 1 tablet: 100 µg (182 % RI), organisk bundet. Ingredienser: ølgær (indeholder byg og hvede), fyldemiddel (mikrokrystallinsk cellulose), '
                      'selenberiget gær, antiklumpningsmidler (magnesiumtrisilikat, magnesiumsalte af fedtsyrer), '
                      'overfladebehandlingsmidler (shellak, ethylcellulose, polyvinylpyrrolidon, polysorbat 80, glycerol, talkum).\n'
                      'Allergener: byg og hvede (i selen-tabletten).\n\nAnsvarlig virksomhed: Zentabox A/S, Unionsvej 4, 4600 Køge (CVR 37447250).\nProduceret af JemoPharm A/S, Hasselvej 1, 4780 Stege.\nKilde: oplysninger fra Zentabox.',
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
