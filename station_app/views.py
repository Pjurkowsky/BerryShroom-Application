from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Station
from .serializers import DashboardSerializer, StationSerializer, SensorSerializer, ValueSerializer


class apiOverviewList(APIView):
    def get(self, request, format=None):
        api_urls = {
            'List': '/station/',
            'Detail Station View': '/station/<str:pk>/',
            'List Station Dashboard View': '/dashboard/',
            'Detail Station-Sensor View': '/station/<str:pk>/<str:pk>',
            'Detail Station-Sensor-Value View': '/station/value/<str:pk>/<str:pk>/',
            'Create Station': '/station-create/',
            'Create Sensor': '/sensor-create/<str:pk>/',
            'Create Value': '/value-create/<str:pk>/<str:pk>/',
            'Update Station': '/station-update/<str:pk>/',
            'Update Sensor': '/sensor-update/<str:pk>/<str:pk>/',
            'Delete Station': '/station-delete/<str:pk>/',
            'Delete Sensor': '/sensor-delete/<str:pk>/<str:pk>'
        }
        return Response(api_urls)


class DashboardList(APIView):
    def get(self, request, format=None):
        station = Station.objects.all()
        serializer = DashboardSerializer(station, many=True)
        #serializer.context["time"] = Settings.objects.all()[0].time_last
        serializer.context["time"] = 24
        return Response(serializer.data)


class StationList(APIView):
    def get(self, request, format=None):
        station = Station.objects.all()
        serializer = StationSerializer(station, many=True)
        return Response(serializer.data)


class StationDetailView(APIView):
    def get(self, request, pk, format=None):
        station = Station.objects.get(index=pk)
        serializer = StationSerializer(station, many=False)
        return Response(serializer.data)


class SensorDetailView(APIView):
    def get(self, request, pk, id, format=None):
        sensor = Station.objects.get(index=pk).sensors.get(index=id)
        serializer = SensorSerializer(sensor, many=False)
        return Response(serializer.data)


class ValueDetailView(APIView):
    def get(self, request, pk, id, format=None):
        value = Station.objects.get(
            index=pk).sensors.get(index=id).values.all()
        serializer = ValueSerializer(value, many=True)
        return Response(serializer.data)


class StationCreate(APIView):
    def post(self, request, format=None):
        serializer = StationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SensorCreate(APIView):
    def post(self, request, pk, format=None):
        serializer = SensorSerializer(data=request.data)
        serializer.context["station_id"] = pk
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValueCreate(APIView):
    def post(self, request, pk, id, format=None):
        sensor = Station.objects.get(index=pk).sensors.get(index=id)
        serializer = ValueSerializer(data=request.data, instance=sensor)
        serializer.context["station_id"] = pk
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StationUpdate(APIView):
    def post(self, request, pk, format=None):
        station = Station.objects.get(index=pk)
        serializer = StationSerializer(data=request.data, instance=station)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SensorUpdate(APIView):
    def post(self, request, pk, id,  format=None):
        sensor = Station.objects.get(index=pk).sensors.get(index=id)
        serializer = SensorSerializer(data=request.data, instance=sensor)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StationDelete(APIView):
    def delete(self, request, pk, format=None):
        station = Station.objects.get(index=pk)
        station.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SensorDelete(APIView):
    def delete(self, request, pk, id, format=None):
        sensor = Station.objects.get(index=pk).sensors.get(index=id)
        sensor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
