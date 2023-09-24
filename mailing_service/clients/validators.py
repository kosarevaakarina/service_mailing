from rest_framework import serializers


class FirstNameValidator:
    """Валидация имени: имя должно состоять только из букв"""
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        first_name = value.get('first_name')
        if first_name is not None and not first_name.isalpha():
            raise serializers.ValidationError('Имя введено некорректно.')


class LastNameValidator:
    """Валидация фамилии: фамилия должна состоять только из букв"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        last_name = value.get('last_name')
        if last_name is not None and not last_name.isalpha():
            raise serializers.ValidationError('Фамилия введена некорректно.')


class PhoneValidator:
    """Валидация номера телефона: номер телефона должен состоять только из цифр"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        phone = value.get('phone')
        if phone is not None and not (phone.isdigit() and len(phone) == 11):
            raise serializers.ValidationError(
                'Номер телефона введен не корректно. Формат: 7XXXXXXXXXX (X - цифра от 0 до 9)')
