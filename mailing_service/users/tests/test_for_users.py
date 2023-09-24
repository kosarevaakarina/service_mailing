from rest_framework import status

from users.models import User
from users.tests.create_user import UserCreate
from rest_framework.test import APITestCase


class UsersRegisterAPITestCase(APITestCase):
    """Тестирование регистрации пользователя"""

    def test_register_user(self):
        response = self.client.post('/users/register/', {
            "email": "test@test.ru",
            "first_name": "Test",
            "last_name": "Testov",
            "password": "0000",
            "password2": "0000"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_with_fatal_password(self):
        """Тестирование создания пользователя при неверно введенном пароля"""
        response = self.client.post('/users/register/', {
            "email": "test@test.ru",
            "first_name": "Test",
            "last_name": "Testov",
            "password": "0000",
            "password2": "1111"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
            'non_field_errors': ['Пароли не совпадают. Проверьте введенные данные']})

    def test_register_user_with_fatal_first_name(self):
        """Тестирование создания пользователя при неверно введенном имени пользователя"""
        response = self.client.post('/users/register/', {
            "email": "test@test.ru",
            "first_name": "Test&",
            "last_name": "Testov",
            "password": "0000",
            "password2": "0000"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Имя введено некорректно.']})

    def test_register_user_with_fatal_last_name(self):
        """Тестирование создания пользователя при неверно введенной фамилии пользователя"""
        response = self.client.post('/users/register/', {
            "email": "test@test.ru",
            "first_name": "Test",
            "last_name": "Testov!!!!!!!",
            "password": "0000",
            "password2": "0000"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Фамилия введена некорректно.']})


class UserListAPITestCase(UserCreate):
    """Тестирование просмотра пользователей"""

    def test_get_unauth_user(self):
        """Тестирование просмотра пользователей для неавторизованного пользователя"""
        response = self.client.get('/users/', )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Учетные данные не были предоставлены.'})

    def test_get_user(self):
        """Тестирование просмотра пользователей для администратора"""
        self.create_user()
        self.user.is_staff = True
        self.user.save()
        response = self.client.get('/users/', )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{
            'email': 'example@test.ru',
            'first_name': 'Test',
            'last_name': 'Testov',
            'is_active': True}])


class UserRetrieveAPITestCase(UserCreate):
    def retrieve_user(self, user_id):
        return self.client.get(f'/users/{user_id}/', )

    def test_retrieve_user(self):
        """Тестирование просмотра аккаунта пользователя"""
        self.create_user()
        response = self.retrieve_user(self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'email': 'example@test.ru',
            'first_name': 'Test',
            'last_name': 'Testov',
            'is_active': True})


class UserUpdateAPITestCase(UserCreate):
    def test_update_user(self):
        """Тестирование обновления пользователя"""
        self.create_user()
        response = self.client.patch(f'/users/update/{self.user.pk}/', {'email': 'newtest@example.ru'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'email': 'newtest@example.ru',
            'first_name': 'Test',
            'last_name': 'Testov',
            'is_active': True})

    def test_update_seller_user_fatal_first_name(self):
        """Тестирование обновления данных пользователя при неверно введенном имени"""
        self.create_user()
        response = self.client.patch(f'/users/update/{self.user.pk}/', {'first_name': 'Test111'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Имя введено некорректно.']})

    def test_update_seller_user_fatal_last_name(self):
        """Тестирование обновления данных пользователя при неверно введенной фамилии"""
        self.create_user()
        response = self.client.patch(f'/users/update/{self.user.pk}/', {'last_name': 'Testov111'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Фамилия введена некорректно.']})


class UserDestroyAPITestCase(UserCreate):
    """Тестирование удаления пользователя"""

    def test_delete_user(self):
        self.create_user()
        response = self.client.delete(f'/users/delete/{self.user.id}/', )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UserManagerTestCase(APITestCase):
    """Тестирование создание пользователя и суперпользователя"""

    def test_user_manager_create_user(self):
        """Тестирование создания пользователя"""
        user = User.objects.create_user(email='test@example.ru', password='test123')
        self.assertTrue(isinstance(user, User))

    def test_user_manager_create_superuser(self):
        """Тестирование создания суперпользователя"""
        user = User.objects.create_superuser(email='test@example.ru', password='test123')
        self.assertTrue(isinstance(user, User))
