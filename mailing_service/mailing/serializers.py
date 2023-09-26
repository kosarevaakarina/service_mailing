from rest_framework import serializers
from clients.serializers import ClientSerializer
from mailing.models import Mailing, MailingLog, Statistics
from mailing.services.periodic_task import create_mailing_on_phone, update_mailing_on_phone


class MailingSerializer(serializers.ModelSerializer):
    """Сериализатор для представления создания рассылки"""

    class Meta:
        model = Mailing
        fields = ['create_at', 'frequency', 'status', 'tag', 'message', 'finish_at']

    def create(self, validated_data):
        """При создании рассылки создается периодическая задача и меняется статус рассылки"""
        mailing = Mailing.objects.create(**validated_data)

        # создание рассылки (периодической задачи)
        create_mailing_on_phone(mailing)
        return mailing

    def update(self, instance, validated_data):
        """При обновлении рассылки удаляется ранее созданная и создается новая периодическая задача"""

        # удаление старых задач
        update_mailing_on_phone(instance)

        super().update(instance, validated_data)

        # изменение созданной рассылки
        create_mailing_on_phone(instance)

        return instance

    def validate(self, attrs):
        """Валидация на создание дублей рассылок"""
        frequency = attrs.get('frequency', None)
        tag = attrs.get('tag', None)
        message = attrs.get('message', None)
        if Mailing.objects.filter(frequency=frequency, tag=tag, message=message).exists():
            raise serializers.ValidationError('Такая рассылка уже существует!')
        return attrs


class MailingRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для представления одной рассылки"""

    class Meta:
        model = Mailing
        fields = '__all__'


class MailingLogSerializer(serializers.ModelSerializer):
    """Сериализатор для представления статистики рассылок"""

    class Meta:
        model = MailingLog
        fields = ('status', 'server_response', 'date_time')


class MailingLogRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для представления статистики одной рассылки"""
    mailing = MailingRetrieveSerializer(read_only=True)
    client = ClientSerializer(read_only=True)

    class Meta:
        model = MailingLog
        fields = ('date_time', 'status', 'server_response', 'mailing', 'client')


class StatisticsSerializer(serializers.ModelSerializer):
    """Сериализатор для представления общей статистики по рассылкам"""
    class Meta:
        model = Statistics
        fields = '__all__'
