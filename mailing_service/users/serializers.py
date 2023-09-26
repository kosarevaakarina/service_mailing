import logging
from rest_framework import serializers
from clients.validators import FirstAndLastNameValidator
from users.models import User

logger = logging.getLogger("base")


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_active')
        validators = [FirstAndLastNameValidator(field='first_name'), FirstAndLastNameValidator(field='last_name')]

    def update(self, instance, validated_data):
        logger.info(f"Пользователь {instance.email} (ID={instance.pk}) обновил информацию")
        super().update(instance, validated_data)
        return instance


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2')
        validators = [FirstAndLastNameValidator(field='first_name'), FirstAndLastNameValidator(field='last_name')]

    def validate(self, attrs):
        """Валидация паролей"""
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Пароли не совпадают. Проверьте введенные данные")
        return attrs

    def save(self, *args, **kwargs):
        """Метод для сохранения нового пользователя"""
        user = User.objects.create(
            email=self.validated_data.get('email'),
            first_name=self.validated_data.get('first_name'),
            last_name=self.validated_data.get('last_name'),
        )
        # Сохраняем пароль
        password = self.validated_data.get('password')
        user.set_password(password)
        user.save()
        logger.info(f"Пользователь {self.validated_data['email']} зарегистрировался")
        return user
