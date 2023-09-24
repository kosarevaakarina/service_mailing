from rest_framework import status

from users.tests.create_user import UserCreate


class ClientCreateAPITestCase(UserCreate):
    """Тестирование регистрации клиентов"""

    def test_create_client_unauth_user(self):
        """Тестирование регистрации клиентов для неавторизованного пользователя"""
        response = self.client.post('/client/', {
            'phone': '78888888888',
            'phone_code': '888',
            'first_name': 'First',
            'last_name': 'Last',
            'tag': 'Active client',
            'timezone': 'Europe/Moscow'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Учетные данные не были предоставлены.'})

    def test_create_client(self):
        """Тестирование регистрации клиента для авторизованного пользователя"""
        self.save_user_for_client()
        response = self.client.post('/client/', {
            'phone': '78888888888',
            'phone_code': '888',
            'first_name': 'First',
            'last_name': 'Last',
            'tag': 'Active client',
            'timezone': 'Europe/Moscow'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_client_with_fatal(self):
        """Тестирование регистрации клиента при неверно введенных данных"""
        self.save_user_for_client()
        response = self.client.post('/client/', {
            'phone': '79995545Q!',
            'phone_code': '999',
            'first_name': 'First1',
            'last_name': 'Last1',
            'tag': 'Active client',
            'timezone': 'Europe/Moscow'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {'non_field_errors': [
                             'Имя введено некорректно.',
                             'Фамилия введена некорректно.',
                             'Номер телефона введен не корректно. Формат: 7XXXXXXXXXX (X - цифра от 0 до 9)']})


class ClientListAPITestCase(UserCreate):
    """Тестирование просмотра клиентов"""

    def get_client(self):
        return self.client.get('/client/')

    def test_get_client_unauth_user(self):
        """Тестирование просмотра клиентов для неавторизованного пользователя"""
        response = self.get_client()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Учетные данные не были предоставлены.'})

    def test_get_client(self):
        """Тестирование просмотра клиентов для авторизованного пользователя"""
        self.save_user_for_client()
        response = self.get_client()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{
            'phone': '79999999999',
            'phone_code': '999',
            'first_name': 'Test',
            'last_name': 'Testov',
            'tag': 'Active client',
            'timezone': 'Europe/Moscow',
            'is_active': True}])


class ClientRetrieveAPITestCase(UserCreate):
    """Тестирование просмотра одного клиента"""

    def retrieve_client(self, id):
        return self.client.get(f'/client/{id}/')

    def test_retrieve_client_unauth_user(self):
        """Тестирование просмотра одного клиента для неавторизованного пользователя"""
        response = self.retrieve_client(1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Учетные данные не были предоставлены.'})

    def test_retrieve_client(self):
        """Тестирование просмотра одного клиента для авторизованного пользователя"""
        self.save_user_for_client()
        response = self.retrieve_client(self.service_client.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'phone': '79999999999',
            'phone_code': '999',
            'first_name': 'Test',
            'last_name': 'Testov',
            'tag': 'Active client',
            'timezone': 'Europe/Moscow',
            'is_active': True})


class ClientUpdateAPITestCase(UserCreate):
    """Тестирование обновления данных о клиенте"""

    def update_client(self, id):
        return self.client.patch(f'/client/{id}/', {'first_name': "NewName"})

    def test_update_client_unauth_user(self):
        """Тестирование обновления данных о клиенте для неавторизованного пользователя"""
        response = self.update_client(1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Учетные данные не были предоставлены.'})

    def test_update_client(self):
        """Тестирование обновления данных о клиенте для авторизованного пользователя"""
        self.save_user_for_client()
        response = self.update_client(self.service_client.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'phone': '79999999999',
            'phone_code': '999',
            'first_name': 'NewName',
            'last_name': 'Testov',
            'tag': 'Active client',
            'timezone': 'Europe/Moscow',
            'is_active': True})


class ClientDestroyAPITestCase(UserCreate):
    """Тестирование удаления клиента"""

    def delete_client(self, id):
        return self.client.delete(f'/client/{id}/')

    def test_delete_client_unauth_user(self):
        """Тестирование удаления клиента для неавторизованного пользоватея"""
        response = self.delete_client(1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Учетные данные не были предоставлены.'})

    def test_delete_client(self):
        """Тестирование удаления клиента для авторизованного пользователя"""
        self.save_user_for_client()
        response = self.delete_client(self.service_client.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
