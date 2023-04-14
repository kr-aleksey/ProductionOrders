from django.contrib import admin

from .models import Category, MeasurementUnit, Order, OrderProduct, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    fields = ('name', 'parent')
    # readonly_fields = ('uid_erp',)


@admin.register(MeasurementUnit)
class MeasurementUnitAdmin(admin.ModelAdmin):
    fields = ('name', 'uid_erp')
    readonly_fields = ('uid_erp',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'counterparty', 'in_stock')
    list_editable = ('counterparty', 'in_stock')
    list_filter = ('in_stock', 'counterparty')
    search_fields = ('name',)
    fields = ('name',
              'category',
              'counterparty',
              'pack_quantity',
              'measurement_unit',
              'in_stock',
              'uid_erp')
    readonly_fields = ('uid_erp',)


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    fields = ('product', 'quantity')

    def __init__(self, parent_model, admin_site, counterparty=None):
        self.counterparty = counterparty
        super().__init__(parent_model, admin_site)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            kwargs["queryset"] = (Product
                                  .objects
                                  .filter(counterparty=self.counterparty))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('number',
                    'counterparty',
                    'customer',
                    'status',
                    'created_at',)
    list_filter = ('status', 'counterparty',)
    date_hierarchy = 'created_at'
    search_fields = ('number',)
    fields = ('number',
              'counterparty',
              'customer',
              'created_at',
              'note',
              'status',)
    readonly_fields = ('number',
                       'counterparty',
                       'customer',
                       'created_at',
                       'note',)

    def get_inline_instances(self, request, obj=None):
        return [
            OrderProductInline(self.model,
                               self.admin_site,
                               counterparty=obj.counterparty)
        ]
