"""Refill logic: the first box ships full packs, later boxes only what the customer is about to run out of.

Supplements come in packs of 30–180 units, so shipping a new pack every month would mean waste and a much
higher price. We keep a per-customer ledger of shipped packs and include an item only when the supply will not
last until the following box (+ a small buffer). Goodies are always included.
"""
import math
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal

from catalog.models import Item

SHIP_INTERVAL_DAYS = 30
BUFFER_DAYS = 7


@dataclass
class Line:
    item: Item
    quantity: int
    units_per_day: Decimal
    reason: str


def supply_until(order, as_of: date) -> dict:
    """Date until which the customer has supply of each item, based on everything shipped so far."""
    from .models import ShipmentLine

    until = {}
    lines = (ShipmentLine.objects.filter(shipment__order=order).select_related('shipment', 'item')
             .order_by('shipment__created_at'))
    for line in lines:
        if line.item.kind != Item.KIND_SUPPLEMENT or not line.item.units_per_pack or not line.units_per_day:
            continue
        shipped = (line.shipment.shipped_at or line.shipment.created_at).date()
        start = max(until.get(line.item_id, shipped), shipped)
        days = int(line.quantity * line.item.units_per_pack / float(line.units_per_day))
        until[line.item_id] = start + timedelta(days=days)
    return until


def _in_week_window(window: str, order, ship_date: date, pkg) -> bool:
    """Goodies tagged "10–13" are only sent in pregnancy weeks 10–13 (Late Care rotates its goodies by week)."""
    try:
        lo, hi = (int(x) for x in window.replace('-', '–').split('–'))
    except ValueError:
        return True
    if order.due_date:
        week = int(40 - (order.due_date - ship_date).days / 7) + 1
    else:
        week = pkg.week_start or 0
    week = min(max(week, pkg.week_start or week), pkg.week_end or week)
    return lo <= week <= hi


def box_contents(order, ship_date: date | None = None, ledger: dict | None = None) -> list[Line]:
    ship_date = ship_date or date.today()
    pkg = order.package_for_shipment(ship_date)
    if pkg is None:
        return []
    single = order.plan == order.PLAN_SINGLE
    ledger = supply_until(order, ship_date) if ledger is None else ledger
    need_until = ship_date + timedelta(days=SHIP_INTERVAL_DAYS + BUFFER_DAYS)
    lines = []
    for c in pkg.contents.select_related('item'):
        item = c.item
        if getattr(order, 'skip_calcium', False) and item.nutrient.lower().startswith('calcium'):
            continue
        if item.kind == Item.KIND_SUPPLEMENT and not c.sst_core and not getattr(order, 'include_extras', True):
            continue
        if item.kind == Item.KIND_GOODIE:
            if c.short_dose and not _in_week_window(c.short_dose, order, ship_date, pkg):
                continue
            lines.append(Line(item, 1, Decimal('0'), 'Goodie'))
            continue
        have = ledger.get(item.pk)
        if not single and have and have >= need_until:
            continue
        per_pack_days = (item.units_per_pack / float(c.units_per_day)) if item.units_per_pack and c.units_per_day else SHIP_INTERVAL_DAYS
        if single or have is None:
            # First shipment of an item: enough for one interval; the next box tops up if needed.
            missing_days = SHIP_INTERVAL_DAYS
        else:
            missing_days = SHIP_INTERVAL_DAYS + BUFFER_DAYS - max(0, (have - ship_date).days)
        qty = max(1, math.ceil(missing_days / per_pack_days))
        lines.append(Line(item, qty, c.units_per_day, 'Ny' if have is None else 'Genopfyldning'))
    return lines


def create_shipment(order, ship_date: date | None = None):
    from .models import Shipment, ShipmentLine

    ship_date = ship_date or date.today()
    lines = box_contents(order, ship_date)
    shipment = Shipment.objects.create(order=order, package=order.package_for_shipment(ship_date))
    for ln in lines:
        ShipmentLine.objects.create(shipment=shipment, item=ln.item, quantity=ln.quantity,
                                    units_per_day=ln.units_per_day, reason=ln.reason)
    return shipment


def simulate(order, start: date, months: int):
    """Dry-run a subscription month by month without touching the database (used for pricing/economics)."""
    ledger, out = {}, []
    for i in range(months):
        d = start + timedelta(days=SHIP_INTERVAL_DAYS * i)
        pkg = order.package_for_shipment(d)
        lines = box_contents(order, d, ledger=ledger)
        for ln in lines:
            if ln.item.kind == Item.KIND_SUPPLEMENT and ln.item.units_per_pack and ln.units_per_day:
                s = max(ledger.get(ln.item.pk, d), d)
                ledger[ln.item.pk] = s + timedelta(days=int(ln.quantity * ln.item.units_per_pack / float(ln.units_per_day)))
        out.append((d, pkg, lines))
    return out
