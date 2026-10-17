from django.conf import settings


def site(request):
    return {
        'COMPANY': settings.COMPANY,
        'STRIPE_ENABLED': settings.STRIPE_ENABLED,
        'CUSTOMER_PORTAL_URL': settings.STRIPE_CUSTOMER_PORTAL_URL,
        'SMILEY_URL': settings.SMILEY_URL,
    }
