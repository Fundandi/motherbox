from datetime import date

from django.contrib import admin, messages
from django.template.response import TemplateResponse
from django.urls import path

from . import fulfilment
from .models import CustomerRequest, Order, Shipment, ShipmentLine, StripeEvent


class ShipmentInline(admin.TabularInline):
    model = Shipment
    extra = 0
    fields = ['package', 'created_at', 'shipped_at', 'tracking_number', 'note']
    readonly_fields = ['created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['reference', 'created_at', 'status', 'plan', 'name', 'email', 'start_package', 'current_box', 'amount']
    list_filter = ['status', 'plan', 'start_package']
    search_fields = ['reference', 'email', 'name', 'stripe_customer_id', 'stripe_subscription_id']
    readonly_fields = ['reference', 'created_at', 'updated_at', 'stripe_session_id', 'stripe_customer_id', 'stripe_subscription_id']
    inlines = [ShipmentInline]
    actions = ['create_shipments']
    change_list_template = 'admin/orders/order/change_list.html'

    @admin.display(description='Boks i dag')
    def current_box(self, obj):
        pkg = obj.package_for()
        return pkg.label if pkg else '—'

    @admin.action(description='Opret forsendelse (med refill-beregnet indhold) for valgte ordrer')
    def create_shipments(self, request, queryset):
        n = 0
        for order in queryset.filter(status__in=['paid', 'demo']):
            if order.package_for_shipment():
                fulfilment.create_shipment(order)
                n += 1
        self.message_user(request, f'{n} forsendelser oprettet. Husk at udfylde track & trace og afsendt-dato.', messages.SUCCESS)

    def get_urls(self):
        return [path('pakkeliste/', self.admin_site.admin_view(self.packing_list), name='orders_packing_list')] + super().get_urls()

    def packing_list(self, request):
        """Who gets what this month (refill-aware) + purchasing totals."""
        today = date.today()
        rows, totals = [], {}
        for o in Order.objects.filter(status='paid').select_related('start_package'):
            if o.plan == Order.PLAN_SINGLE and o.shipments.exists():
                continue
            already = o.shipments.filter(created_at__year=today.year, created_at__month=today.month).exists()
            lines = [] if already else fulfilment.box_contents(o, today)
            rows.append({'order': o, 'package': o.package_for_shipment(today), 'already': already, 'lines': lines})
            for ln in lines:
                totals[ln.item] = totals.get(ln.item, 0) + ln.quantity
        ctx = {
            **self.admin_site.each_context(request),
            'title': f'Pakkeliste {today:%d.%m.%Y}',
            'rows': rows,
            'items': sorted(totals.items(), key=lambda kv: (kv[0].kind, kv[0].name)),
        }
        return TemplateResponse(request, 'admin/orders/packing_list.html', ctx)


class ShipmentLineInline(admin.TabularInline):
    model = ShipmentLine
    extra = 0


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    inlines = [ShipmentLineInline]
    list_display = ['order', 'package', 'created_at', 'shipped_at', 'tracking_number']
    list_filter = ['package', 'shipped_at']
    search_fields = ['order__reference', 'order__email', 'tracking_number']


@admin.register(StripeEvent)
class StripeEventAdmin(admin.ModelAdmin):
    list_display = ['event_id', 'type', 'received_at']
    readonly_fields = ['event_id', 'type', 'received_at']


@admin.register(CustomerRequest)
class CustomerRequestAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'kind', 'reference', 'email', 'handled', 'result']
    list_filter = ['kind', 'handled']
    search_fields = ['reference', 'email', 'name']
    readonly_fields = ['created_at']
