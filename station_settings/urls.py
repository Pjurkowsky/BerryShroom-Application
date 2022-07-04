from django.contrib import admin
from django.urls import path, include

from station_settings import views

urlpatterns = [
    path('settings/',
         views.SettingsList.as_view(), name="dashboard"),
    path('settings/<str:pk>/',
         views.SettingsDetailView.as_view(), name="dashboard"),

]
