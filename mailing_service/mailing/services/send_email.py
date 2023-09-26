import logging
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from mailing.models import MailingLog

logger = logging.getLogger("base")


def get_mailing_log(owner) -> list:
    """Получает логи о рассылке, которые были сделаны за последние 24 часа"""

    # получает всю информацию о рассылках для конкретного пользователя
    mailing_logs = MailingLog.objects.filter(mailing__owner=owner)
    mailing_log_list = []
    for mailing_log in mailing_logs:
        mailing_date = mailing_log.date_time.replace(tzinfo=None)
        date_now = datetime.now().replace(tzinfo=None)
        delta = (date_now - mailing_date).total_seconds()

        # проверяет прошло ли 86400 секунд с момента создания информации о рассылки
        if int(delta) < 86400:
            mailing_log_list.append(mailing_log)
    return mailing_log_list


def create_message(mailing_log_lst: list) -> str:
    """Формирует сообщение для рассылки"""
    message = 'Рассылки за сегодня:\n'
    count = 1
    for mailing_log in mailing_log_lst:
        mailing = mailing_log.mailing
        date_time = mailing_log.date_time.strftime("%H:%M.%S")
        status = mailing_log.status
        server_response = mailing_log.server_response
        client = mailing_log.client
        # формирование сообщения для конкретного пользователя по созданным рассылкам
        message += (f'{count}. {mailing}. Клиент: {client}. Время рассылки: {date_time}. Статус отправки: {status}. '
                    f'Ответ сервера: {server_response}.\n')
        count += 1
    return message


def get_owner() -> list:
    """Формирование рассылки для конкретного пользователя"""
    mailing_logs = MailingLog.objects.all()
    owner_list = []
    data_list = []
    for mailing_log in mailing_logs:
        owner_list.append(mailing_log.mailing.owner)

        # получаем весь список пользователей, которые имеют информацию о рассылках
        owner_list = list(set(owner_list))
        for owner in owner_list:
            mailing_log_list = get_mailing_log(owner)
            message = create_message(mailing_log_list)

            # получаем словарь с данными о сообщении и пользователе
            data = {
                'message': message,
                'owner': owner
            }
            data_list.append(data)
    return data_list


def send_message_email() -> None:
    """Отправляет сообщение пользователю с информацией о рассылках за последние сутки"""
    current_date = datetime.now().date()
    current_date = current_date.strftime("%d.%m.%Y")
    subject = f'Информация о рассылках за {current_date}'
    data_list = get_owner()
    for data in data_list:
        message = data['message']
        owner = data['owner']
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[owner.email]
            )
            logger.info(f"Сообщение о рассылках за последние сутки пользователю {owner.email} отправлено")
        except Exception:
            logger.error(f"Сообщение о рассылках за последние сутки пользователю {owner.email} не отправлено")
            raise 'Сообщение не отправлено'
