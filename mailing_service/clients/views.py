from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from clients.models import Client
from clients.serializers import ClientSerializer


class ClientViewset(viewsets.ModelViewSet):
    """Представление для модели клиента"""
    model = Client
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Пользователь может видеть только тех клиентов, которых он сам зарегистрировал"""
        user = self.request.user
        if user.is_staff:
            return Client.objects.all()
        else:
            return Client.objects.filter(user=user, is_active=True)

    def perform_create(self, serializer):
        """Привязка пользователя к зарегистрированному клиенту"""
        serializer.save(user=self.request.user)
