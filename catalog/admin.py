from django.contrib import admin

from .models import Item, Manufacturer, Package, PackageItem


class PackageItemInline(admin.TabularInline):
    model = PackageItem
    extra = 0
    autocomplete_fields = ['item']
    fields = ['position', 'item', 'daily_dose', 'sst_core', 'cost_share', 'purpose']


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['position', 'label', 'title', 'weeks_label', 'price', 'estimated_cost', 'is_active']
    list_display_links = ['label', 'title']
    list_editable = ['price', 'is_active']
    inlines = [PackageItemInline]

    @admin.display(description='Indkøb (udsalgspris)')
    def estimated_cost(self, obj):
        return f'{obj.cost_price()} kr.'


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'review_platform', 'review_rating', 'review_count', 'review_checked']
    search_fields = ['name']
    prepopulated_fields = {'slug': ['name']}


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'kind', 'nutrient', 'manufacturer', 'pack_size', 'retail_price', 'retailer', 'verified']
    list_filter = ['kind', 'verified', 'manufacturer']
    search_fields = ['name', 'nutrient', 'manufacturer__name']
    prepopulated_fields = {'slug': ['name']}
