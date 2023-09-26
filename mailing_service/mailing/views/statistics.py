from rest_framework.generics import ListAPIView

from mailing.models import Statistics
from mailing.serializers import StatisticsSerializer


class StatisticsListAPIView(ListAPIView):
    """Представление для просмотра общей статистики по всем рассылкам"""
    model = Statistics
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
