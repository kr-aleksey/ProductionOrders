from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from orders.models import Cart

from .models import Counterparty, User


@admin.register(Counterparty)
class CounterpartyAdmin(admin.ModelAdmin):
    fields = ('name',)


class CartInline(admin.TabularInline):
    model = Cart
    fields = ('product', 'quantity')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    search_fields = ('first_name',
                     'last_name',
                     'counterparty__name')
    list_display = ('first_name',
                    'last_name',
                    'counterparty',
                    'is_active',
                    'is_staff',
                    'is_superuser')
    ordering = ('email',)
    inlines = (CartInline,)
    fieldsets = (
        (
            None,
            {'fields': ('email', 'password')}
        ),
        (
            'Персональные данные',
            {'fields': ('first_name', 'last_name', 'counterparty')}
        ),
        (
            'Права',
            {
                'fields': ('is_active', 'is_staff', 'is_superuser'),
            }
        ),
        (
            'Даты',
            {'fields': ('last_login', 'date_joined')}
        ),
    )
