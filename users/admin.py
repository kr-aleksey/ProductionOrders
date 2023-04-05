from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Counterparty, User


@admin.register(Counterparty)
class CounterpartyAdmin(admin.ModelAdmin):
    fields = ('name',)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    search_fields = ('first_name',
                     'last_name',
                     'username',
                     'counterparty__name')
    list_display = ('username',
                    'first_name',
                    'last_name',
                    'is_active',
                    'is_staff',
                    'is_superuser')
