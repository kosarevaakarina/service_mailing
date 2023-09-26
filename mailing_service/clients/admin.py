from django.contrib import admin

from clients.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Административная панель для модели Client"""
    list_display = ('first_name', 'last_name', 'tag')
    fieldsets = (
        (None, {'fields': ('phone', )}),
        ('Персональные данные', {'fields': ('first_name', 'last_name', 'tag', 'timezone', 'user')}),
        ('Код мобильного оператора', {'fields': ('phone_code', )}),
    )
