from django.urls import path
from station_app import views


urlpatterns = [
    path('', views.apiOverviewList.as_view(), name="station-api-overview"),
    path('station/', views.StationList.as_view(), name="station-list"),
    path('station/<str:pk>/', views.StationDetailView.as_view(),
         name="station-detailview"),
    path('station/<str:pk>/<str:id>/',
         views.SensorDetailView.as_view(), name="sensor-detailview"),
    path('station/value/<str:pk>/<str:id>/',
         views.ValueDetailView.as_view(), name="value-detailview"),
    path('station-create/', views.StationCreate.as_view(), name="station-create"),
    path('sensor-create/<str:pk>/',
         views.SensorCreate.as_view(), name="sensor-create"),
    path('value-create/<str:pk>/<str:id>/',
         views.ValueCreate.as_view(), name="value-create"),
    path('station-update/<str:pk>/',
         views.StationUpdate.as_view(), name="station-update"),
    path('sensor-update/<str:pk>/<str:id>/',
         views.SensorUpdate.as_view(), name="sensor-update"),
    path('station-delete/<str:pk>/',
         views.StationDelete.as_view(), name="station-delete"),
    path('sensor-delete/<str:pk>/<str:id>/',
         views.SensorDelete.as_view(), name="sensor-delete"),
    path('dashboard/',
         views.DashboardList.as_view(), name="dashboard"),
]
