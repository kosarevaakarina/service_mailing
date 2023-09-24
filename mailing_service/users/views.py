from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser

from users.models import User
from users.permissions import IsUser
from users.serializers import UserRegisterSerializer, UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """Представление для регистрации пользователя"""
    model = User
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer


class UserListAPIView(generics.ListAPIView):
    """Представления для просмотра списка пользователей"""
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Представление для просмотра одного пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsUser]


class UserUpdateAPIView(generics.UpdateAPIView):
    """Представление для обновления пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsUser]


class UserDestroyAPIView(generics.DestroyAPIView):
    """Представление для удаления пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsUser]
