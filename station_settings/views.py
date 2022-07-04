from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Group
from .serializers import GroupSerializer


class apiOverviewList(APIView):
    def get(self, request, format=None):
        api_urls = {
            'List': '/settings/',
        }
        return Response(api_urls)


class SettingsList(APIView):
    def get(self, request, format=None):
        group = Group.objects.all()
        serializer = GroupSerializer(group, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SettingsDetailView(APIView):
    def get(self, request, pk, format=None):
        try:
            group = Group.objects.get(id=pk)
        except Group.DoesNotExist:
            group = None
        serializer = GroupSerializer(group, many=False)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        group = Group.objects.get(id=pk)
        serializer = GroupSerializer(data=request.data, instance=group)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            group = Group.objects.get(name=pk)
            group.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
