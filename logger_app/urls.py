from django.urls import path, include
from logger_app import views


urlpatterns = [
    path('', views.LogList.as_view(), name='logs'),
]
