from users.tests.create_user import UserCreate
from rest_framework import status
from datetime import datetime


class MailingCreateAPITestCase(UserCreate):
    """Тестирование создания рассылки"""
    def test_create_mailing_unauth_user(self):
        """Тестирование создания рассылки неавторизованным пользователем"""
        response = self.client.post('/create/', {
            'frequency': "DAY",
            'tag': 'Active client',
            'message': 'Test message',
            'finish_at': datetime(year=2024, month=1, day=1)
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Учетные данные не были предоставлены.'})

    def test_create_mailing(self):
        """Тестирование создания рассылки авторизованным пользователем"""
        self.save_user_for_mailing()
        response = self.client.post('/create/', {
            'frequency': "DAY",
            'tag': 'Active client',
            'message': 'Test message',
            'finish_at': datetime(year=2024, month=1, day=1)
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            'frequency': 'DAY',
            'status': 'CREATE',
            'tag': 'Active client',
            'message': 'Test message',
            'finish_at': '2024-01-01T00:00:00Z'})


class MailingListAPITestCase(UserCreate):
    """Тестирование просмотра рассылок"""
    def get_mailing(self):
        return self.client.get('')

    def test_get_mailing_unauth_user(self):
        """Тестирование просмотра рассылок для неавторизованного пользователя"""
        response = self.get_mailing()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Учетные данные не были предоставлены.'})

    def test_get_mailing(self):
        self.save_user_for_mailing()
        response = self.get_mailing()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{
            'frequency': 'DAY',
            'status': 'CREATE',
            'tag': 'Active client',
            'message': 'Test message',
            'finish_at': '2024-01-01T00:00:00Z'}])


class MailingRetrieveAPITestCase(UserCreate):
    """Тестирование просмотра одной рассылки"""
    def retrieve_mailing(self, mailing_id):
        return self.client.get(f'/mailing/{mailing_id}/')

    def test_retrieve_mailing_unauth_user(self):
        """Тестирование просмотра одной рассылки для неавторизованного пользователя"""
        response = self.retrieve_mailing(self.mailing.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Учетные данные не были предоставлены.'})

    def test_retrieve_mailing(self):
        """Тестирование просмотра одной рассылки для авторизованного пользователя"""
        self.mailing = self.save_user_for_mailing()
        response = self.retrieve_mailing(self.mailing.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MailingUpdateAPITestCase(UserCreate):
    """Тестирование обновления информации о рассылке"""
    def update_mailing(self, mailing_id):
        return self.client.patch(f'/mailing/update/{mailing_id}/', {'frequency': 'WEEK'})

    def test_update_mailing_unauth_user(self):
        response = self.update_mailing(self.mailing.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Учетные данные не были предоставлены.'})

    def test_update_mailing(self):
        self.save_user_for_mailing()
        response = self.update_mailing(self.mailing.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'frequency': 'WEEK',
            'status': 'CREATE',
            'tag': 'Active client',
            'message': 'Test message',
            'finish_at': '2024-01-01T00:00:00Z'})


class MailingDestroyAPITestCase(UserCreate):
    """Тестирование удаления рассылки"""

    def delete_mailing(self, mailing_id):
        return self.client.delete(f'/mailing/delete/{mailing_id}/')

    def test_delete_mailing_unauth_user(self):
        response = self.delete_mailing(self.mailing.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_mailing(self):
        self.save_user_for_mailing()
        response = self.delete_mailing(self.mailing.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
