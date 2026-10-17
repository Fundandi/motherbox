import os
from decimal import Decimal

# Motherbox has one subscription price for all boxes. The Basis/Komplet split was dropped when every box became a single
# 30-day Zentabox pack; the `extras` arguments are kept so existing call sites keep working.


def subscription_price(stage: str | None = None, extras: bool = True) -> Decimal:
    """Monthly subscription price (DKK incl. moms, free shipping)."""
    if stage == 'ttc':
        return Decimal(os.environ.get('SUBSCRIPTION_PRICE_TTC', os.environ.get('SUBSCRIPTION_MONTHLY_PRICE', '349')))
    return Decimal(os.environ.get('SUBSCRIPTION_MONTHLY_PRICE', '349'))


def single_price(package, extras: bool = True) -> Decimal:
    return package.price


def has_extras(package) -> bool:
    return package.contents.filter(item__kind='supplement', sst_core=False).exists()
