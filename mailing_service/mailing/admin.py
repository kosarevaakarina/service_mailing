from django.contrib import admin
from mailing.models import Mailing, MailingLog, Statistics


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('message', 'status', 'tag')
    fieldsets = (
        (None, {'fields': ('message', )}),
        ('Информация о рассылке', {'fields': ('frequency', 'status', 'tag')}),
        ('Пользователь', {'fields': ('owner', )}),
        ('Признак активности', {'fields': ('is_active', )}),
    )


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'status', 'server_response')


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('create_at', 'tag', 'count')
