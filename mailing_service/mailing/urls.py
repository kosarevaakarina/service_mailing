from django.urls import path

from mailing.views.mailing import (MailingCreateAPIView, MailingRetrieveAPIView, MailingUpdateAPIView,
                                   MailingDestroyAPIView, MailingListAPIView)
from mailing.views.mailing_log import MailingLogListAPIView, MailingLogRetrieveAPIView

urlpatterns = [
    path('create/', MailingCreateAPIView.as_view(), name='mailing_create'),
    path('', MailingListAPIView.as_view(), name='mailing_list'),
    path('<int:pk>/', MailingRetrieveAPIView.as_view(), name='mailing_detail'),
    path('update/<int:pk>/', MailingUpdateAPIView.as_view(), name='mailing_update'),
    path('delete/<int:pk>/', MailingDestroyAPIView.as_view(), name='mailing_update'),
    path('mailing_log/', MailingLogListAPIView.as_view(), name='mailing_log_list'),
    path('mailing_log/<int:pk>/', MailingLogRetrieveAPIView.as_view(), name='mailing_log_retrieve'),
]
