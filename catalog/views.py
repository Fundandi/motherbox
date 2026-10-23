from datetime import date

from django.contrib import messages
from django.db.models import Count, Min, Prefetch
from django.shortcuts import get_object_or_404, redirect, render

from .models import Advisor, Item, Manufacturer, Package, PackageItem, package_for_due_date
from .pricing import subscription_price
from .sources import SOURCES, SST_BASELINE
from .visuals import nutrient_style


WHY_ROWS = [
    'Følger Sundhedsstyrelsens anbefalinger',
    'Bokse, der skifter med din graviditetsuge',
    'Én dagspose – 30 poser pr. boks',
    'Produceret i Danmark af JemoPharm',
    'Fuld varedeklaration før køb',
    'Goodies i hver boks · ingen binding',
]


def _active_packages():
    return Package.objects.filter(is_active=True)


def home(request):
    packages = _active_packages().prefetch_related(
        Prefetch('contents', queryset=PackageItem.objects.select_related('item'))
    )
    # Which box covers which of Sundhedsstyrelsen's recommendations, with the amount in the daily pack.
    lines = {p.pk: [ln for c in p.contents.all() if c.item.kind == Item.KIND_SUPPLEMENT for ln in c.item.nutrient_lines]
             for p in packages}
    for p in packages:
        p.key_lines = lines[p.pk][:4]
    sst_rows = []
    for row in SST_BASELINE:
        prefixes = ('d-vitamin', 'd3-vitamin') if row['nutrient'] == 'D-vitamin' else (row['nutrient'].lower(),)
        boxes = []
        for p in packages:
            hit = next((ln for ln in lines[p.pk] if ln['name'].lower().startswith(prefixes)), None)
            boxes.append({'label': p.label, 'amount': hit['amount'] if hit else None})
        sst_rows.append(dict(row, boxes=boxes))
    manufacturers = (
        Manufacturer.objects.filter(items__kind=Item.KIND_SUPPLEMENT, items__in_packages__package__is_active=True)
        .annotate(n=Count('items__in_packages', distinct=True)).filter(n__gt=0).order_by('-n', 'name')
    )
    return render(request, 'catalog/home.html', {
        'packages': packages,
        'manufacturers': manufacturers,
        'advisors': Advisor.objects.filter(is_active=True),
        'sub_price': subscription_price(),
        'ttc_price': subscription_price('ttc'),
        'basis_price': subscription_price(None, extras=False),
        'min_single_price': packages.aggregate(m=Min('price'))['m'],
        'sst_baseline': SST_BASELINE,
        'sst_rows': sst_rows,
        'why_rows': WHY_ROWS,
    })


def start(request):
    """Route the visitor to the right box: trying to conceive, pregnant (due date) or postpartum."""
    if request.method != 'POST':
        return redirect('home')
    stage = request.POST.get('stage', 'pregnant')
    if stage == Package.STAGE_TTC:
        pkg = _active_packages().filter(stage=Package.STAGE_TTC).first()
        return redirect(pkg) if pkg else redirect('package_list')
    if stage == Package.STAGE_POSTPARTUM:
        pkg = _active_packages().filter(stage=Package.STAGE_POSTPARTUM).first()
        return redirect(pkg) if pkg else redirect('package_list')

    try:
        due_date = date.fromisoformat(request.POST.get('due_date', ''))
    except ValueError:
        messages.error(request, 'Angiv venligst en gyldig terminsdato.')
        return redirect('/#bokse')
    pkg, week = package_for_due_date(due_date)
    if pkg is None:
        messages.error(request, 'Vi kunne ikke finde en pakke til den dato. Se alle pakker nedenfor.')
        return redirect('package_list')
    request.session['due_date'] = due_date.isoformat()
    request.session['pregnancy_week'] = round(week, 1)
    request.session['recommended_slug'] = pkg.slug
    return redirect(pkg)


def package_list(request):
    return render(request, 'catalog/package_list.html', {
        'packages': _active_packages().prefetch_related(
            Prefetch('contents', queryset=PackageItem.objects.select_related('item'))
        ),
        'sub_price': subscription_price(),
    })


def package_detail(request, slug):
    package = get_object_or_404(Package, slug=slug, is_active=True)
    all_packages = list(_active_packages())
    idx = next(i for i, p in enumerate(all_packages) if p.pk == package.pk)
    supplements = list(package.supplements)
    for c in supplements:
        c.style = nutrient_style(c.item.nutrient)
        c.lines = [dict(line, style=nutrient_style(line['name'])) for line in c.item.nutrient_lines]
    goodies = list(package.goodies)
    # Late Care rotates goodies by pregnancy week ("10–13" in short_dose): group them for display.
    goodie_windows = {}
    for g in goodies:
        if g.short_dose:
            goodie_windows.setdefault(g.short_dose, []).append(g)
    unique_goodies = list({g.item_id: g for g in goodies}.values())
    return render(request, 'catalog/package_detail.html', {
        'package': package,
        'supplements': supplements,
        'goodies': unique_goodies,
        'goodie_windows': [{'weeks': w, 'items': items} for w, items in goodie_windows.items()],
        'prev_pkg': all_packages[idx - 1] if idx > 0 else None,
        'next_pkg': all_packages[idx + 1] if idx + 1 < len(all_packages) else None,
        'all_packages': all_packages,
        'is_recommended': request.session.get('recommended_slug') == package.slug,
        'pregnancy_week': request.session.get('pregnancy_week'),
        'sub_price': subscription_price(package.stage),
        'sources': SOURCES,
        'why_rows': WHY_ROWS,
        'min_single_price': package.price,
        'sst_lines': [ln for c in supplements for ln in c.lines if ln['sst']],
        'extra_lines': [ln for c in supplements for ln in c.lines if not ln['sst']],
        'nutrient_count': sum(len(c.lines) for c in supplements),
    })


def manufacturer_list(request):
    manufacturers = Manufacturer.objects.filter(items__in_packages__package__is_active=True).distinct().prefetch_related(
        Prefetch('items', queryset=Item.objects.filter(in_packages__package__is_active=True).distinct()
                 .prefetch_related('in_packages__package'))
    )
    return render(request, 'catalog/manufacturer_list.html', {'manufacturers': manufacturers})


def manufacturer_detail(request, slug):
    manufacturer = get_object_or_404(Manufacturer, slug=slug)
    items = manufacturer.items.prefetch_related('in_packages__package')
    return render(request, 'catalog/manufacturer_detail.html', {'manufacturer': manufacturer, 'items': items})


def science(request):
    packages = list(_active_packages().prefetch_related(
        Prefetch('contents', queryset=PackageItem.objects.select_related('item').filter(item__kind=Item.KIND_SUPPLEMENT))
    ))
    # Nutrient × box matrix built from each box's daily pack (nutrients in order of first appearance)
    per_box = []
    nutrients = []
    for p in packages:
        amounts = {}
        for c in p.contents.all():
            for line in c.item.nutrient_lines:
                amounts[line['name']] = line['amount'] or '✓'
                if line['name'] not in nutrients:
                    nutrients.append(line['name'])
        per_box.append(amounts)
    matrix = [{'nutrient': n, 'style': nutrient_style(n), 'sst': n.lower().startswith(Item.SST_NUTRIENTS),
               'cells': [box.get(n) for box in per_box]} for n in nutrients]
    return render(request, 'catalog/science.html', {
        'sources': SOURCES,
        'sst_baseline': SST_BASELINE,
        'packages': packages,
        'matrix': matrix,
    })


def page(request, template):
    return render(request, f'pages/{template}.html', {'sub_price': subscription_price(), 'ttc_price': subscription_price('ttc')})
