from rest_framework.generics import ListAPIView, RetrieveAPIView

from mailing.models import MailingLog
from mailing.serializers import MailingLogSerializer, MailingLogRetrieveSerializer


class MailingLogListAPIView(ListAPIView):
    """Представление для просмотров статистики рассылок"""
    model = MailingLog
    serializer_class = MailingLogSerializer
    queryset = MailingLog.objects.all()


class MailingLogRetrieveAPIView(RetrieveAPIView):
    """Представление для просмотра статистики одной рассылки"""
    model = MailingLog
    serializer_class = MailingLogRetrieveSerializer
    queryset = MailingLog.objects.all()
