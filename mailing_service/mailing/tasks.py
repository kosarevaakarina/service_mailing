from celery import shared_task
from mailing.services.send_email import send_message_email
from mailing.services.send_message_phone import send_message_to_phone


@shared_task(name='send_message')
def send_message(mailing_id, client_id):
    """Периодическая задача: Отправка клиентам сообщений по номеру телефона"""
    send_message_to_phone(mailing_id, client_id)


@shared_task(name='send_email')
def send_message_by_email():
    """Периодическая задача: Ежедневная отправка сообщений пользователям о совершенных рассылках,
        регистрируется через административную панель"""
    send_message_email()
