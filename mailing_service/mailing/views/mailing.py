from rest_framework import generics

from mailing.models import Mailing
from mailing.permissions import IsOwner
from mailing.serializers import MailingSerializer, MailingRetrieveSerializer
from rest_framework.permissions import IsAuthenticated


class MailingCreateAPIView(generics.CreateAPIView):
    """Представление для создания рассылки"""
    model = Mailing
    serializer_class = MailingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, status='CREATE')


class MailingListAPIView(generics.ListAPIView):
    """Представление для просмотра рассылок"""
    model = Mailing
    serializer_class = MailingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingRetrieveAPIView(generics.RetrieveAPIView):
    """Представление для просмотра одной рассылки"""
    model = Mailing
    serializer_class = MailingRetrieveSerializer
    queryset = Mailing.objects.all()
    permission_classes = [IsOwner]


class MailingUpdateAPIView(generics.UpdateAPIView):
    """Представление для обновления рассылки"""
    model = Mailing
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()
    permission_classes = [IsOwner]


class MailingDestroyAPIView(generics.DestroyAPIView):
    """Представление для удаления рассылки"""
    model = Mailing
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()
    permission_classes = [IsOwner]
