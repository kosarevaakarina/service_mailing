import logging
from rest_framework import serializers
from clients.models import Client
from clients.validators import FirstNameValidator, LastNameValidator, PhoneValidator

logger = logging.getLogger("base")


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

    def create(self, validated_data):
        logger.info(f"Добавлен клиент {validated_data['first_name']} {validated_data['last_name']}")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        logger.info(f"Информация о клиенте {instance.first_name} {instance.last_name} (ID={instance.pk}) обновлена")
        super().update(instance, validated_data)
        return instance
