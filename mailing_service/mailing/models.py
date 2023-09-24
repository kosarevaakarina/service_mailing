import logging
from django.db import models
from config import settings
from clients.models import ClientRoles, Client, NULLABLE
from mailing.services.periodic_task import delete_task

logger = logging.getLogger("base")


class Mailing(models.Model):
    """Модель рассылки"""

    FREQUENCY = [
        ('DAY', 'раз в день'),
        ('WEEK', 'раз в неделю'),
        ('MONTH', 'раз в месяц')
    ]

    STATUS = [
        ('FINISH', 'завершена'),
        ('CREATE', 'создана'),
        ('START', 'запущена')
    ]

    create_at = models.DateTimeField(verbose_name='Дата и время запуска рассылки')
    frequency = models.CharField(max_length=100, choices=FREQUENCY, verbose_name='Периодичность')
    status = models.CharField(max_length=100, choices=STATUS, verbose_name='Статус', **NULLABLE)
    tag = models.CharField(max_length=50, choices=ClientRoles.TAGS, verbose_name='тэг клиента')
    message = models.TextField(verbose_name='Сообщение')
    finish_at = models.DateTimeField(verbose_name='Дата и время завершения рассылки')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE)

    is_active = models.BooleanField(default=True, verbose_name='признак активности')

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ('create_at',)

    def __str__(self):
        """Строковое представление экземпляров модели Mailing"""
        return f'Рассылка сообщения {self.message} для пользователей: {self.tag}'

    def delete(self, using=None, keep_parents=False):
        """Функция, делающая рассылку не активной"""
        self.is_published = False
        self.status = 'FINISH'
        self.save()
        delete_task(self)
        logger.info(f'Удалена рассылка ID={self.pk}')


class MailingLog(models.Model):
    """Модель логов рассылки"""

    STATUS = [
        ('Success', 'успешно'),
        ('Failure', 'отказ')
    ]

    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время отправки')
    status = models.CharField(max_length=100, choices=STATUS, verbose_name='Статус попытки')
    server_response = models.TextField(verbose_name='Ответ почтового сервера', **NULLABLE)
    mailing = models.ForeignKey(Mailing, on_delete=models.SET_NULL, verbose_name='Рассылка', **NULLABLE)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, verbose_name='Клиент', **NULLABLE)

    class Meta:
        verbose_name = 'лог отправки письма'
        verbose_name_plural = 'логи отправок писем'

    def __str__(self):
        return f'Информация о рассылке {self.mailing.pk}'
