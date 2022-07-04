from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Station
from .serializers import StationSerializer, RelaySerializer


class apiOverviewList(APIView):
    def get(self, request, format=None):
        api_urls = {
            'List': '/mushstation',
            'Detail Station View': '/mushstation/<str:pk>/',
            'Detail Station-Relay View': '/mushstation/<str:pk>/<str:pk>',
            'Create Station': '/mushstation-create/',
            'Create Relay': '/relay-create/<str:pk>/',
            'Update Station': '/mushstation-update/<str:pk>/',
        }
        return Response(api_urls)


class MushStationList(APIView):
    def get(self, request, format=None):
        station = Station.objects.all()
        serializer = StationSerializer(station, many=True)
        return Response(serializer.data)


class MushStationDetailView(APIView):
    def get(self, request, pk, format=None):
        station = Station.objects.get(index=pk)
        serializer = StationSerializer(station, many=False)
        return Response(serializer.data)


class MushStationCreate(APIView):
    def post(self, request, format=None):
        serializer = StationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MushStationUpdate(APIView):
    def post(self, request, pk, format=None):
        station = Station.objects.get(pk=pk)
        serializer = StationSerializer(data=request.data, instance=station)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RelayDetailView(APIView):
    def get(self, request, pk, id, format=None):
        relay = Station.objects.get(index=pk).relays.get(index=id)
        serializer = RelaySerializer(relay, many=False)
        return Response(serializer.data)


class RelayCreate(APIView):
    def post(self, request, pk, format=None):
        serializer = RelaySerializer(data=request.data)
        serializer.context["station_id"] = pk
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RelayUpdate(APIView):
    def post(self, request, pk, id, format=None):
        relay = Station.objects.get(index=pk).relays.get(index=id)
        serializer = RelaySerializer(data=request.data, instance=relay)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
