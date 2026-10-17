"""Public sources and Sundhedsstyrelsen's baseline. Every figure is traceable to a URL (checked 2026-09-30)."""

SST_URL = 'https://www.sst.dk/vidensbase/graviditet-og-smaaboern/graviditet/ernaering-mad-og-maaltider-til-gravide-og-ammende'
FVST_GRAVID_URL = 'https://foedevarestyrelsen.dk/kost-og-foedevarer/alt-om-mad/de-officielle-kostraad/kostraad-til-dig/gravid-eller-ammende'

SST_BASELINE = [
    {'nutrient': 'Folsyre', 'dose': '400 µg dagligt', 'period': 'Fra du planlægger graviditet til og med uge 12', 'url': SST_URL},
    {'nutrient': 'D-vitamin', 'dose': '10 µg dagligt', 'period': 'Hele graviditeten og mens du ammer', 'url': SST_URL},
    {'nutrient': 'Jern', 'dose': '40–50 mg dagligt', 'period': 'Fra uge 10 til fødslen', 'url': SST_URL},
    {'nutrient': 'Calcium', 'dose': '500 mg dagligt', 'period': 'Kun hvis du får mindre end ½ liter mælk (eller tilsvarende) om dagen', 'url': SST_URL},
]

SOURCES = [
    {'title': 'Ernæring, mad og måltider til gravide og ammende', 'publisher': 'Sundhedsstyrelsen', 'url': SST_URL, 'year': ''},
    {'title': 'Sunde vaner før, under og efter graviditet (8. udgave)', 'publisher': 'Sundhedsstyrelsen',
     'url': 'https://www.sst.dk/media/s5cjdmjj/sunde_vaner_8_-udgave-2022.pdf', 'year': '2022'},
    {'title': 'Kostråd: Gravid eller ammende', 'publisher': 'Fødevarestyrelsen', 'url': FVST_GRAVID_URL, 'year': ''},
    {'title': 'Kosttilskudsanbefalinger', 'publisher': 'Fødevarestyrelsen',
     'url': 'https://foedevarestyrelsen.dk/kost-og-foedevarer/alt-om-mad/kosttilskud/kosttilskudsanbefalinger', 'year': ''},
    {'title': 'Ernærings- og sundhedsanprisninger', 'publisher': 'Fødevarestyrelsen',
     'url': 'https://foedevarestyrelsen.dk/kost-og-foedevarer/maerkning-og-markedsfoering-af-foedevarer/frivillig-foedevareinformation/ernaerings-og-sundhedsanprisninger', 'year': ''},
    {'title': 'EU Register of nutrition and health claims', 'publisher': 'Europa-Kommissionen',
     'url': 'https://ec.europa.eu/food/food-feed-portal/screen/health-claims/eu-register', 'year': ''},
    {'title': 'Dietary Reference Values for nutrients (inkl. øvre grænser)', 'publisher': 'EFSA',
     'url': 'https://www.efsa.europa.eu/en/topics/topic/dietary-reference-values', 'year': ''},
]
