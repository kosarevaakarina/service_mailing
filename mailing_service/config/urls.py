from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    # docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),

    # admin
    path('admin/', admin.site.urls),

    # apps
    path('users/', include('users.urls'), name='users'),
    path('mailing/', include('mailing.urls'), name='mailing'),
    path('client/', include('clients.urls'), name='client'),
]
