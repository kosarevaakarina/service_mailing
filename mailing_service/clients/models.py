import logging
import pytz
from django.conf import settings
from django.db import models

logger = logging.getLogger("base")


NULLABLE = {'blank': True, 'null': True}


class ClientRoles:
    """Класс, описывающий роли клиентов"""
    POTENTIAL_CLIENT = 'Potential client'
    ACTIVE_CLIENT = 'Active client'
    FORMER_CLIENT = 'Former client'

    TAGS = [
        (POTENTIAL_CLIENT, 'Potential client'),
        (ACTIVE_CLIENT, 'Active client'),
        (FORMER_CLIENT, 'Former client')
    ]


class Client(models.Model):
    """Модель клиента"""

    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    phone = models.CharField(unique=True, max_length=11, verbose_name='номер телефона')
    phone_code = models.CharField(max_length=3, verbose_name='код мобильного оператора')
    first_name = models.CharField(max_length=50, verbose_name='имя клиента')
    last_name = models.CharField(max_length=50, verbose_name='фамилия клиента')
    tag = models.CharField(max_length=50, choices=ClientRoles.TAGS, verbose_name='тэг клиента')
    timezone = models.CharField(max_length=50, choices=TIMEZONES, verbose_name='часовой пояс')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                             verbose_name='пользователь')

    is_active = models.BooleanField(default=True, verbose_name='активность клиента')

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self) -> str:
        """Строковое представление экземпляра модели Client"""
        return f'{self.first_name} {self.last_name} ({self.phone})'

    def delete(self, using=None, keep_parents=False) -> None:
        """При удалении клиента меняет статус активности на False"""
        self.is_active = False
        self.save()
        logger.info(f"Пользователь {self.user.email} удалил клиента {self.first_name} {self.last_name}")
