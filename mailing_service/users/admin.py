from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Административная панель для модели User"""
    list_display = ('first_name', 'last_name', 'email')
