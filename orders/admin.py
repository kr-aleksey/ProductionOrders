from django.contrib import admin

from .models import (Category,
                     Nomenclature,
                     Order,
                     OrderNomenclature,
                     MeasurementUnit)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'uid_erp')
    readonly_fields = ('uid_erp',)


@admin.register(MeasurementUnit)
class MeasurementUnitAdmin(admin.ModelAdmin):
    fields = ('name', 'uid_erp')
    readonly_fields = ('uid_erp',)


@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    fields = ('name', 'measurement_unit', 'in_stock', 'uid_erp')
    readonly_fields = ('uid_erp',)


class OrderNomenclatureInline(admin.TabularInline):
    model = OrderNomenclature
    fields = ('order', 'nomenclature', 'amount', '')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ('number',
              'counterparty',
              'customer',
              'status',
              'created_at',
              'note')
    readonly_fields = ('created_at',)
    # inlines = (OrderNomenclatureInline,)
    list_display = ('number',
                    'counterparty',
                    'customer',
                    'status',
                    'created_at')
