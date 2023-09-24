from datetime import datetime
import pytz
from django_celery_beat.models import CrontabSchedule, PeriodicTask


class MessageService:
    """Сервис создания рассылки"""
    def __init__(self, mailing):
        """Инициализация рассылки по экземпляру модели Mailing"""
        self.mailing = mailing

    def create_task(self):
        """Создание периодической задачи"""
        crontab = self.crontab_create()
        PeriodicTask.objects.create(crontab=crontab, name=str(self.mailing.pk), task='send_message',
                                    args=[self.mailing.pk])

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

        schedule, _ = CrontabSchedule.objects.get_or_create(minute=minute, hour=hour, day_of_week=day_of_week,
                                                            day_of_month=day_of_month, month_of_year='*')

        return schedule


def finish_task(mailing, client):
    """Возвращает True или False в зависимости от даты и времени завершения рассылки"""
    end_time = mailing.finish_at
    end_time = end_time.replace(tzinfo=pytz.timezone(client.timezone))
    current_time = datetime.now(pytz.timezone(client.timezone))
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    return str(end_time) < str(current_time)


def delete_task(mailing):
    """Удаление периодической задачи"""
    task = PeriodicTask.objects.get(name=str(mailing.pk))
    task.delete()
    mailing.status = 'FINISH'
    mailing.delete()
