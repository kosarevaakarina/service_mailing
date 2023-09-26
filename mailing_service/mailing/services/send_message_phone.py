import logging
import requests
from django.conf import settings
from clients.models import Client
from mailing.models import MailingLog, Mailing, Statistics
from mailing.services.periodic_task import finish_task, delete_task, MessageService

logger = logging.getLogger("base")


class SendMessageService:
    """Сервис для рассылки клиентам сообщений с помощью стороннего сервиса"""
    # токен для работы с сервисом
    TOKEN = settings.SEND_MESSAGE_TOKEN
    # заголовок для авторизации
    headers = {'Authorization': f'Bearer {TOKEN}'}
    # базовый url
    BASE_URL = settings.BASE_URL_SEND_MESSAGE

    def __init__(self, mailing: Mailing, client: Client) -> None:
        """Инициализация сервиса экземплярами модели Mailing и Client"""
        self.mailing = mailing
        self.client = client
        self.mailing_log = None
        self.response = None

    def send_message_phone(self) -> None:
        """Отправка сообщения с помощью стороннего сервиса"""
        id_message = self.mailing.pk
        phone = int(self.client.phone)
        message = self.mailing.message
        data_json = {
            "id": id_message,
            "phone": phone,
            "message": message
        }
        self.BASE_URL = f'{self.BASE_URL}{id_message}'
        try:
            self.response = requests.post(self.BASE_URL, headers=self.headers, json=data_json)

            logger.info(
                f"Сообщение клиенту {self.client.first_name} {self.client.last_name} на номер {phone} отправлено")

        except Exception:

            logger.error(
                f"Сообщение клиенту {self.client.first_name} {self.client.last_name} на номер {phone} не отправлено")

            raise 'Сообщение на указанный номер телефона не доставлено!'

        if self.response.status_code == 200:
            self.mailing_log_success()
            self.create_or_update_statistics()
        else:
            self.mailing_log_fatal()

    def create_mailing_log(self, status: str):
        """Создание информации о рассылке """
        self.mailing_log = MailingLog.objects.create(
                status=status,
                server_response=self.response.reason,
                mailing=self.mailing,
                client=self.client
            )

    def mailing_log_success(self) -> None:
        """Создание информации о рассылке со статусом Success"""
        self.create_mailing_log(status='Success')
        logger.info(f"Информация о рассылке {self.mailing.id} создана ID={self.mailing_log.pk}")

    def mailing_log_fatal(self) -> None:
        """Создание информации о рассылке со статусом Failure"""
        self.create_mailing_log(status='Failure')
        logger.error(f"Информация о рассылке {self.mailing.id} не создана")

    def create_or_update_statistics(self):
        """Сбор общей статистики по рассылкам"""
        if Statistics.objects.filter(tag=self.mailing.tag).exists():
            statistics = Statistics.objects.get(tag=self.mailing.tag)
            statistics.increment_count()
        else:
            statistics = Statistics.objects.create(tag=self.mailing.tag)
            statistics.increment_count()

            logger.info(f"Создание статистики ID={statistics.pk}")


def send_message_to_phone(mailing_id, client_id):
    """Отправка сообщения клиенту на номер телефона"""
    mailing = Mailing.objects.get(pk=mailing_id)
    client = Client.objects.get(pk=client_id)
    message_service = MessageService(mailing, client)
    if finish_task(mailing, client):
        # если время рассылки закончилось, то она удаляется
        delete_task(mailing, client)
    elif message_service.check_create_at():
        # если время запуска рассылки настало, то отправляем сообщения
        sending = SendMessageService(mailing, client)
        sending.send_message_phone()
