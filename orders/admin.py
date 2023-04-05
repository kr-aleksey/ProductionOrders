from django.contrib import admin

from .models import (Category,
                     Product,
                     Order,
                     OrderProduct,
                     MeasurementUnit)


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
    fields = ('name',
              'category',
              'counterparty',
              'measurement_unit',
              'in_stock',
              'uid_erp')
    readonly_fields = ('uid_erp',)


# class OrderProductInline(admin.TabularInline):
#     model = OrderProduct
#     fields = ('order', 'product', 'amount', '')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ('number',
              'counterparty',
              'customer',
              'status',
              'created_at',
              'note')
    readonly_fields = ('created_at',)
    list_display = ('number',
                    'counterparty',
                    'customer',
                    'status',
                    'created_at')
