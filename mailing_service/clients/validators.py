from rest_framework import serializers


class FirstAndLastNameValidator:
    """Валидация имени: имя должно состоять только из букв"""
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if self.field is not None and not self.field.isalpha():
            raise serializers.ValidationError(f'Поле {self.field} введено некорректно.')


class PhoneValidator:
    """Валидация номера телефона: номер телефона должен состоять только из цифр"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        phone = value.get('phone')
        if phone is not None and not (phone.isdigit() and len(phone) == 11):
            raise serializers.ValidationError(
                'Номер телефона введен не корректно. Формат: 7XXXXXXXXXX (X - цифра от 0 до 9)')
