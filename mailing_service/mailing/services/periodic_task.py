import logging
from datetime import datetime
import pytz
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from clients.models import Client
from mailing.models import Mailing

logger = logging.getLogger("base")


class MessageService:
    """Сервис создания рассылки"""

    def __init__(self, mailing, client):
        """Инициализация рассылки по экземпляру модели Mailing"""
        self.mailing = mailing
        self.client = client

    def create_periodic_task(self):
        """Создание периодической задачи"""
        crontab = self.crontab_create()
        periodic_task = PeriodicTask.objects.update_or_create(
            crontab=crontab,
            name=f'Рассылка №{self.mailing.pk} для клиента ID={self.client.pk}',
            task='send_message',
            args=[self.mailing.pk, self.client.pk])

        logger.info(f"Создана периодическая задача: {periodic_task[0].name}")

    def crontab_create(self):
        """Создание CRONTAB для выполнения периодической задачи"""
        minute = self.mailing.create_at.minute
        hour = self.mailing.create_at.hour
        if self.mailing.frequency == 'DAY':
            day_of_week = '*'
            day_of_month = '*'

        elif self.mailing.frequency == 'WEEK':
            day_of_week = self.mailing.create_at.weekday()
            day_of_month = '*'

        else:
            day_of_week = '*',
            day_of_month = self.mailing.create_at.day if self.mailing.create_at.day <= 28 else 28

        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=minute,
            hour=hour,
            day_of_week=day_of_week,
            day_of_month=day_of_month,
            month_of_year='*',
            timezone=self.client.timezone)

        return schedule

    def check_create_at(self):
        """Проверяет время начала рассылки, возвращает True если дата и время рассылки меньше настоящего времени"""
        create_at = self.mailing.create_at
        create_at = create_at.replace(tzinfo=pytz.timezone(self.client.timezone))
        current_time = datetime.now(pytz.timezone(self.client.timezone))
        current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        return str(create_at) < str(current_time)

    def create_task(self):
        """Создание задачи по рассылке сообщения"""
        # проверяем дату и время создания рассылки
        if self.check_create_at():
            # создание периодической задачи для смс-рассылки конкретному клиенту
            self.create_periodic_task()

            # изменение статуса рассылки
            self.mailing.status = 'START'
            self.mailing.save()


def finish_task(mailing, client):
    """Возвращает True или False в зависимости от даты и времени завершения рассылки"""
    end_time = mailing.finish_at
    end_time = end_time.replace(tzinfo=pytz.timezone(client.timezone))
    current_time = datetime.now(pytz.timezone(client.timezone))
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    return str(end_time) < str(current_time)


def delete_task(mailing, client):
    """Удаление периодической задачи"""
    if PeriodicTask.objects.filter(name=f'Рассылка №{mailing.pk} для клиента ID={client.pk}').exists():
        task = PeriodicTask.objects.get(name=f'Рассылка №{mailing.pk} для клиента ID={client.pk}')
        task.delete()
        logger.info(f"Периодическая задача ID={task.id} удалена")


def create_mailing_on_phone(mailing):
    """Создает периодическую задачу с рассылкой для клиентов с указанным в рассылке тегом"""
    # получаем всех клиентов по указанному в рассылке тэгу
    clients = Client.objects.filter(tag=mailing.tag, is_active=True)
    if clients.exists():
        for client in clients:
            # для каждого найденного клиента создаем периодическую задачу с учетом часового пояса
            message_service = MessageService(mailing, client)
            message_service.create_task()

            logger.info(f"Создана рассылка ID={mailing.pk} для клиента ID={client.pk}")


def update_mailing_on_phone(mailing):
    """Обновляет периодическую задачу с рассылкой для клиентов с указанным в рассылке тегом"""
    # получаем всех клиентов по указанному в рассылке тэгу
    clients = Client.objects.filter(tag=mailing.tag, is_active=True)
    if clients.exists():
        for client in clients:
            # для каждого найденного клиента удаляем ранее созданные периодические задачи
            delete_task(mailing, client)

            logger.info(f"Обновлена рассылка ID={mailing.pk} для клиента ID={client.pk}")


def create_mailing_for_client(client):
    """Создает периодическую задачу с рассылкой для клиентов с указанным у клиента тегом"""

    # получаем все рассылки для клиента по его тэгу
    mailings = Mailing.objects.filter(tag=client.tag, is_active=True)
    if mailings.exists():
        for mailing in mailings:
            # если рассылки есть, то создаем периодические задачи для смс-рассылки
            message_service = MessageService(mailing, client)
            message_service.create_task()

            logger.info(f"Создана рассылка ID={mailing.pk} для клиента ID={client.pk}")


def update_mailing_for_client(client):
    """Обновляет периодическую задачу с рассылкой для клиентов с указанным у клиента тегом"""
    # получаем все рассылки для клиента по его тэгу
    mailings = Mailing.objects.filter(tag=client.tag, is_active=True)
    if mailings.exists():
        for mailing in mailings:
            # удаляем все имеющиеся периодические задачи
            delete_task(mailing, client)
            # создаем новые периодические задачи по обновленным данным
            create_mailing_for_client(client)

            logger.info(f"Обновлена рассылка ID={mailing.pk} для клиента ID={client.pk}")


