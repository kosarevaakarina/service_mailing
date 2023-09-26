import logging
from rest_framework import serializers
from clients.models import Client
from clients.validators import FirstAndLastNameValidator, PhoneValidator
from mailing.services.periodic_task import create_mailing_for_client, update_mailing_for_client

logger = logging.getLogger("base")


class ClientSerializer(serializers.ModelSerializer):
    """Сериализатор для представления модели"""

    class Meta:
        model = Client
        fields = ('phone', 'phone_code', 'first_name', 'last_name', 'tag', 'timezone', 'is_active')
        validators = [
            FirstAndLastNameValidator(field='first_name'),
            FirstAndLastNameValidator(field='last_name'),
            PhoneValidator(field='phone')
        ]

    def create(self, validated_data):
        """Создание клиента: при создании клиента проверяется наличие рассылки для данной категории клиентов и при её
            наличии создается периодическая задача для её осуществления с учетом часового пояса клиента"""

        client = Client.objects.create(**validated_data)

        logger.info(f"Добавлен клиент {validated_data['first_name']} {validated_data['last_name']}")

        # создание рассылки для клиента
        create_mailing_for_client(client)

        return client

    def update(self, instance, validated_data):
        """Обновление информации о клиенте: при обновлении информации клиента проверяется наличие рассылки для данного
            клиента и её обновлении (при изменении номера телефона, тэга или часового пояса)"""

        logger.info(f"Информация о клиенте {instance.first_name} {instance.last_name} (ID={instance.pk}) обновлена")

        super().update(instance, validated_data)

        # если у клиента поменялся тэг, часовой пояс или номер телефона, рассылка обновляется
        tag = validated_data.get('tag', None)
        timezone = validated_data.get('timezone', None)
        phone = validated_data.get('phone', None)

        if tag is not None or timezone is not None or phone is not None:
            update_mailing_for_client(instance)

        return instance
