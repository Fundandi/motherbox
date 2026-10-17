# Motherbox

Månedlige bokse med kosttilskud (i producenternes originale pakninger) + goodies. Der er 11 bokse: *Klar til graviditet*, graviditetsmåned 2–10 (uge 5–40) og *Efter fødslen*.

Teknik: Django 5.2, Tailwind (CDN), Stripe Checkout (abonnement og engangskøb), WhiteNoise og Postgres i produktion.

## Kør lokalt

```bash
cd care
python3.13 -m venv venv
venv/bin/pip install -r requirements.txt
cp .env.example .env                        # udfyld værdierne
venv/bin/python manage.py migrate
venv/bin/python manage.py seed_catalog      # producenter, produkter og de 11 pakker
venv/bin/python manage.py createsuperuser   # login til /admin
venv/bin/python manage.py runserver
```

Uden Stripe-nøgler kører checkout i **demo-tilstand**. Der bliver ikke trukket penge, og ordren gemmes med status "Demo".

Tests: `venv/bin/python manage.py test`

## Sådan hænger det sammen

| Del | Fil |
|---|---|
| Datamodel: Producent → Produkt → Pakke (+ indhold, dosis, SST/tillæg) | `catalog/models.py` |
| Alt indhold (producenter, produkter, links, priser, anmeldelser, pakker) | `catalog/seed_data.py`, `catalog/seed_packages.py` |
| Terminsdato → boks | `catalog.models.package_for_due_date` |
| Stripe Checkout + webhooks | `orders/stripe_service.py`, `orders/views.py` |
| Refill-logik (sender kun det, kunden er ved at løbe tør for) | `orders/fulfilment.py` |
| Pakkeliste og indkøbsbehov i admin | `/admin/orders/order/pakkeliste/` |

Ændringer i admin overskrives ikke af `seed_catalog`. Kør `seed_catalog --update` for at tvinge seed-data igennem.

| Kommando | Formål |
|---|---|
| `python manage.py purchase_list` | Skriver `../Indkøbsliste.md` ud fra kataloget |
| `python manage.py box_economics --wholesale-discount 0.4 --shipping 38 --packaging 5` | Enhedsøkonomi pr. boks for typiske kundeforløb |

**Priser** (miljøvariabler): `SUBSCRIPTION_MONTHLY_PRICE` (Komplet, 449), `BASIS_DISCOUNT` (Basis = Komplet − 50) og `SUBSCRIPTION_PRICE_TTC` (Klar til graviditet, 199). Enkeltbokse sættes pr. pakke i admin.

**Lovkrav, der er bygget ind:** "Fortryd aftale"-knap med "Bekræft fortrydelse" og kvittering på e-mail (`/fortryd-aftale/`). Online opsigelse på samme platform (`/mit-abonnement/`), som opsiger i Stripe med det samme. Separat GDPR-samtykke til terminsdato. Varedeklaration vises før køb. Link til smiley-rapport (`SMILEY_URL`). Kun EU-godkendte anprisninger, og ingen anbefalinger fra sundhedspersoner i markedsføringen.

## Stripe-opsætning (ca. 15 min)

1. Opret en konto på dashboard.stripe.com. Test-tilstand kræver ikke CVR.
2. **Developers → API keys**: kopiér `sk_test_…` og `pk_test_…` til `.env` (`STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`).
3. **Settings → Payment methods**: slå Kort, Apple Pay og Google Pay til. **MobilePay** kan også slås til, men Stripe understøtter det kun ved enkeltkøb, ikke ved månedlige træk.
4. **Settings → Billing → Customer portal**: slå portalen til (opsigelse, betalingskort, fakturaer). Kopiér "Login link" til `STRIPE_CUSTOMER_PORTAL_URL`.
5. **Developers → Webhooks → Add endpoint**: `https://DITDOMÆNE/stripe/webhook/` med events:
   `checkout.session.completed`, `checkout.session.async_payment_succeeded`, `checkout.session.async_payment_failed`,
   `invoice.paid`, `invoice.payment_failed`, `customer.subscription.updated`, `customer.subscription.deleted`.
   Kopiér signing secret til `STRIPE_WEBHOOK_SECRET`.
   Lokalt: `stripe listen --forward-to localhost:8000/stripe/webhook/`
6. Test med kortet `4242 4242 4242 4242`, en vilkårlig fremtidig dato og en vilkårlig CVC.
7. Når CVR og Fødevarestyrelsen-registrering er på plads: aktivér kontoen, og skift til `sk_live_…`, `pk_live_…` og et live-webhook.

Produkter og priser behøver ikke at blive oprettet i Stripe. Checkout sender pris og navn med hver gang.

## Deploy (Render)

`render.yaml` opretter en webservice og en Postgres-database. Sæt `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` (fx `https://motherbox.dk`), `SITE_URL` og Stripe-variablerne. Migrations og seed kører automatisk ved deploy. Railway og Heroku bruger `Procfile`.

## Månedlig drift

1. Admin → Ordrer → **Pakkeliste denne måned**. Den viser, hvad hver kunde skal have, og samlet indkøbsbehov med links.
2. Køb ind (se `../Indkøbsliste.md`).
3. Pak boksene. Markér ordrerne → handlingen **"Opret forsendelse"**. Så gemmes indholdet, og refill-logikken holder styr på næste måned.
4. Udfyld track & trace og afsendt-dato på forsendelsen.
