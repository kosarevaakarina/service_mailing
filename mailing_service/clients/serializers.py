from rest_framework import serializers
from clients.models import Client
from clients.validators import FirstNameValidator, LastNameValidator, PhoneValidator


class ClientSerializer(serializers.ModelSerializer):
    """Сериализатор для представления модели"""
    class Meta:
        model = Client
        fields = ('phone', 'phone_code', 'first_name', 'last_name', 'tag', 'timezone', 'is_active')
        validators = [
            FirstNameValidator(field='first_name'),
            LastNameValidator(field='last_name'),
            PhoneValidator(field='phone')
        ]
