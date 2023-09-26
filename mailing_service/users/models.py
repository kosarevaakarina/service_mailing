import logging
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.manager import UserManager

logger = logging.getLogger("base")


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Модель пользователя"""
    username = None
    email = models.EmailField(unique=True, verbose_name='электронная почта')
    first_name = models.CharField(max_length=50, verbose_name='имя пользователя', **NULLABLE)
    last_name = models.CharField(max_length=50, verbose_name='фамилия пользователя', **NULLABLE)

    is_active = models.BooleanField(default=True, verbose_name='активность пользователя')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        """Строковое представление экземпляров модели User"""
        return self.email

    def delete(self, using=None, keep_parents=False):
        """При удалении экземпляра модели User статус активности изменяется на False"""
        self.is_active = False
        self.save()
        logger.info(f"Пользователь {self.email} удален")
