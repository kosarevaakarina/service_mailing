from celery import shared_task
from clients.models import Client
from mailing.models import Mailing
from mailing.services.periodic_task import finish_task, delete_task
from mailing.services.send_email import send_message_email
from mailing.services.send_message_phone import SendMessageService


@shared_task(name='send_message')
def send_message(mailing_id, client_id):
    """Периодическая задача: Отправка клиентов сообщений по номеру телефона"""
    mailing = Mailing.objects.get(pk=mailing_id)
    client = Client.objects.get(pk=client_id)
    if finish_task(mailing, client):
        delete_task(mailing, client)
    else:
        sending = SendMessageService(mailing, client)
        sending.send_message_phone()


@shared_task(name='send_email')
def send_message_by_email():
    """Периодическая задача: Ежедневная отправка сообщений пользователям о совершенных рассылках"""
    send_message_email()
