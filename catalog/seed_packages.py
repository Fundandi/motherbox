"""Editorial content for the 4 Motherbox boxes. Health statements use EU-authorised claim wording only (Reg. 432/2012 & 1924/2006 art. 14)."""

U = 'https://images.unsplash.com/'

DHA_CLAIM = ('Moderens indtag af docosahexaensyre (DHA) bidrager til normal udvikling af hjernen og øjnene hos fosteret og hos spædbørn, '
             'der ammes. Den gavnlige virkning opnås ved et dagligt indtag på 200 mg DHA ud over det anbefalede daglige indtag af '
             'omega-3-fedtsyrer for voksne, dvs. 250 mg DHA og EPA.')

PACKAGE_TEXTS = [
    {
        'slug': 'klar-til-graviditet', 'position': 0, 'stage': 'ttc', 'month': None, 'week_start': None, 'week_end': None,
        'title': 'Jeg vil gerne blive gravid',
        'tagline': 'Sundhedsstyrelsen anbefaler folsyre, allerede fra du begynder at prøve. Denne boks gør dig klar.',
        'hero_nutrient': 'Folsyre 400 µg',
        'image_url': U + 'photo-1506014299253-3725319c0f69?w=900&q=80&fit=crop',
        'body_now': 'Fosterets neuralrør (anlægget til hjerne og rygmarv) lukker sig allerede omkring dag 28 efter befrugtningen. Mange ved på det tidspunkt endnu ikke, at de er gravide.\n\n'
                    'Derfor anbefaler Sundhedsstyrelsen, at du tager folsyre, allerede fra du begynder at forsøge at blive gravid, og fortsætter til og med uge 12.',
        'why': 'Folsyre er den vigtigste anbefaling før graviditet. Supplerende indtag af folsyre øger folatstatus hos moderen. En lav folatstatus hos moderen er en risikofaktor i forhold til udvikling af neuralrørsdefekter hos det voksende foster. '
               'Anprisningen er rettet mod kvinder i den fødedygtige alder, og den gavnlige virkning opnås ved et dagligt supplerende indtag af 400 µg folsyre i mindst én måned før og op til tre måneder efter undfangelsen.\n\n'
               'Når testen er positiv, skifter dit abonnement automatisk til Early Care.',
    },
    {
        'slug': 'early-care', 'position': 1, 'stage': 'pregnant', 'month': None, 'week_start': 5, 'week_end': 9,
        'title': 'Jubi, vi er gravide',
        'tagline': 'De første uger: hjertet begynder at slå, og for mange topper kvalmen. Folsyre og D-vitamin er kernen.',
        'hero_nutrient': 'Folsyre + D-vitamin',
        'image_url': U + 'photo-1493894473891-10fc1e5dbd22?w=900&q=80&fit=crop',
        'body_now': 'I uge 5–9 dannes fosterets hjerte, og de første organer anlægges. Mange oplever kvalme, som ofte topper omkring uge 8–10.\n\n'
                    'Når du har kvalme, kan det være svært at spise varieret. Så er det rart at have styr på de tilskud, Sundhedsstyrelsen anbefaler – i én daglig pose.',
        'why': 'Sundhedsstyrelsen anbefaler 400 µg folsyre til og med uge 12 og 10 µg D-vitamin hele graviditeten. Begge dele er i dagsposen. Folat bidrager til væksten af moderens væv under graviditeten, og D-vitamin bidrager til normal optagelse og udnyttelse af calcium.\n\n'
               'Ekstra jern venter vi med til uge 10, som Sundhedsstyrelsen anbefaler – så skifter dit abonnement automatisk til Late Care.\n\n'
               'Vi har ikke ingefærtilskud med, fordi danske myndigheder fraråder ingefærkapsler og -shots til gravide. I stedet er der ingefær i almindelig fødevaremængde blandt goodies. Er kvalmen svær, så tal med din læge eller jordemoder.',
    },
    {
        'slug': 'late-care', 'position': 2, 'stage': 'pregnant', 'month': None, 'week_start': 10, 'week_end': 40,
        'title': 'Late Care',
        'tagline': 'Fra uge 10 til fødslen: jern, D-vitamin og DHA i én daglig pose – og goodies, der følger din graviditet måned for måned.',
        'hero_nutrient': 'Jern fra uge 10',
        'image_url': U + 'photo-1541956799312-3f9df99e0006?w=900&q=80&fit=crop',
        'body_now': 'Fra uge 10 stiger din blodvolumen, og den vokser med 40–50 % i løbet af graviditeten. I andet trimester mineraliseres fosterets knogler, og hjernen vokser hurtigt. I tredje trimester lagrer fosteret jern og fedt til de første måneder.\n\n'
                    'Sundhedsstyrelsens anbefalinger er de samme fra uge 10 og helt frem til fødslen. Derfor er dagsposen også den samme – mens goodies og vores brev skifter med din graviditetsuge.',
        'why': 'Sundhedsstyrelsen anbefaler 40–50 mg jern dagligt fra uge 10. Dagsposen indeholder 39 mg jern. Jern bidrager til normal dannelse af røde blodlegemer og hæmoglobin og til normal ilttransport i kroppen. '
               'D-vitamin (10 µg) fortsætter hele graviditeten.\n\n'
               + DHA_CLAIM + ' Dagsposen indeholder 500 mg DHA.\n\n'
               'Dagsposen indeholder 300 mg calcium. Får du mindre end ½ liter mælk eller tilsvarende om dagen, anbefaler Sundhedsstyrelsen 500 mg calcium – tal med os, så finder vi en løsning. '
               'Har din læge eller jordemoder målt din blodprocent og anbefalet en anden jerndosis, skal du følge deres råd.',
    },
    {
        'slug': 'ammeboks', 'position': 3, 'stage': 'postpartum', 'month': None, 'week_start': None, 'week_end': None,
        'title': 'Ammeboksen',
        'tagline': 'Tiden efter fødslen kræver også sit. En boks til dig, der ammer og kommer dig.',
        'hero_nutrient': 'D-vitamin + DHA',
        'image_url': U + 'photo-1542385151-efd9000785a0?w=900&q=80&fit=crop',
        'body_now': 'De første måneder efter fødslen tærer på kroppen: blodtab ved fødslen, amning og lidt søvn. Behovet for flere næringsstoffer er større, mens du ammer.',
        'why': 'Sundhedsstyrelsen anbefaler 10 µg D-vitamin dagligt, mens du ammer. Det er i dagsposen sammen med jod. D-vitamin bidrager til normal funktion af immunsystemet, og jod bidrager til normal produktion af skjoldbruskkirtelhormoner.\n\n'
               + DHA_CLAIM + '\n\nHar du haft et stort blodtab eller lav blodprocent, så følg din læges råd om jern.',
    },
]
