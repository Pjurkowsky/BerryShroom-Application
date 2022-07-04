from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('station_app.urls')),
    path('api-mushfarm/', include('mushfarm.urls')),
    path('api-settings/', include('station_settings.urls')),
    path('api-log/', include('logger_app.urls')),
]
