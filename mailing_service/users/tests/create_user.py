from datetime import datetime, timezone

from rest_framework.test import APITestCase

from clients.models import Client
from mailing.models import Mailing
from users.models import User


class UserCreate(APITestCase):
    def setUp(self):
        """Создание экземпляров моделей Mailing и Client"""
        self.service_client = Client.objects.create(
            phone='79999999999',
            phone_code='999',
            first_name='Test',
            last_name='Testov',
            tag='Active client',
            timezone='Europe/Moscow'
        )

        self.mailing = Mailing.objects.create(
            create_at=datetime(year=2023, month=9, day=29, hour=9, minute=12, second=54).replace(tzinfo=timezone.utc),
            frequency='DAY',
            status='CREATE',
            tag='Active client',
            message='Test message',
            finish_at=datetime(year=2024, month=1, day=1).replace(tzinfo=timezone.utc)
        )

    def create_user(self):
        """Создание и авторизация пользователя"""
        self.email = 'example@test.ru'
        user_data = {
            'email': self.email,
            'first_name': 'Test',
            'last_name': 'Testov'
        }
        self.user = User(**user_data)
        self.user.set_password('123Qaz')
        self.user.save()
        response = self.client.post(
            '/users/token/',
            {
                'email': self.email,
                'password': '123Qaz'
            }
        )
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def save_user_for_client(self):
        """Привязка авторизованного пользователя к его клиенту"""
        self.create_user()
        self.service_client.user = self.user
        self.service_client.save()
        return self.service_client

    def save_user_for_mailing(self):
        """Привязка авторизованного пользователя к созданной им рассылке"""
        self.create_user()
        self.mailing.owner = self.user
        self.mailing.save()
        return self.mailing
