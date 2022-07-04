from django.urls import path, include

from mushfarm import views


urlpatterns = [
    path('', views.apiOverviewList.as_view(), name='mushstation-api-overview'),
    path('mushstation/', views.MushStationList.as_view(), name="mushstation-list"),
    path('mushstation/<str:pk>/', views.MushStationDetailView.as_view(),
         name="mushstation-detailview"),
    path('mushstation-create/', views.MushStationCreate.as_view(),
         name="mushstation-create"),
    path('mushstation-update/<str:pk>/', views.MushStationUpdate.as_view(),
         name="mushstation-update"),
    path('mushstation/<str:pk>/<str:id>/', views.RelayDetailView.as_view(),
         name="relay-detailview"),
    path('relay-create/<str:pk>/', views.RelayCreate.as_view(),
         name="relay-create"),
    path('relay-update/<str:pk>/<str:id>/', views.RelayUpdate.as_view(),
         name="relay-update"),
]
