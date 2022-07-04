from rest_framework import serializers
from .models import Log


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ('id', 'logger', 'message', 'datetime')

    def create(self, validated_data):
        log = Log.objects.create(**validated_data)
        log.save()
        return log
