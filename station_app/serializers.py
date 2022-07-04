from rest_framework import serializers

from .models import Station, Sensor, Value
from datetime import datetime, timedelta

from django.db.models import Max, Min


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = ('value', 'date_created')

    def update(self, instance, valideted_data):
        sensor = instance
        value = Value.objects.create(**valideted_data)
        value.save()
        sensor.values.add(value.id)
        station = Station.objects.get(index=self.context["station_id"])
        station.date_created = datetime.now()
        station.save()
        return value


class SensorSerializer(serializers.ModelSerializer):
    values = ValueSerializer(many=True)

    class Meta:
        model = Sensor
        fields = ('index', 'id', 'name', 'display_name',
                  'type', 'show', 'values')

    def create(self, validated_data):
        values_data = validated_data.pop('values')
        sensor = Station.objects.get(
            index=self.context["station_id"]).sensors.create(**validated_data)
        sensor.save()
        return sensor

    def update(self, instance, validated_data):
        instance.display_name = validated_data.get(
            'display_name', instance.display_name)
        instance.show = validated_data.get('show', instance.show)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance


class StationSerializer(serializers.ModelSerializer):
    sensors = SensorSerializer(many=True)

    class Meta:
        model = Station
        fields = ('index', 'id', 'name', 'display_name',
                  'delay_time', 'show', 'date_created', 'sensors')

    def create(self, validated_data):
        sensors_data = validated_data.pop('sensors')
        station = Station.objects.create(**validated_data)
        station.save()
        for sensor_data in sensors_data:
            values_data = sensor_data.pop('values')
            sensor = Sensor.objects.create(**sensor_data)
            station.sensors.add(sensor.id)
            for value_data in values_data:
                value = Value.objects.create(**value_data)
                sensor.values.add(value.id)
        return station

    def update(self, instance, validated_data):
        sensors_data = validated_data.pop('sensors')
        instance.name = validated_data.get('name', instance.name)
        instance.display_name = validated_data.get(
            'display_name', instance.display_name)
        instance.delay_time = validated_data.get(
            'delay_time', instance.delay_time)
        instance.show = validated_data.get('show', instance.show)
        instance.save()

        return instance


class DashboardSensorSerializer(serializers.ModelSerializer):

    value = serializers.SerializerMethodField('get_last_value')
    value_date = serializers.SerializerMethodField('get_last_value_date')
    max_value = serializers.SerializerMethodField('get_max_value')
    max_value_date = serializers.SerializerMethodField('get_max_value_date')
    min_value = serializers.SerializerMethodField('get_min_value')
    min_value_date = serializers.SerializerMethodField('get_min_value_date')

    def get_last_value(self, sensor):
        value = sensor.values.order_by('-date_created')
        return value[0].value if value.__len__() >= 1 else None

    def get_last_value_date(self, sensor):
        value_date = sensor.values.order_by('-date_created')
        return value_date[0].date_created if value_date.__len__() >= 1 else None

    def get_max_value(self, sensor):
        time_treshold = datetime.now() - timedelta(hours=self.context['time'])
        return sensor.values.filter(date_created__gt=time_treshold).aggregate(Max('value'))['value__max']

    def get_max_value_date(self, sensor):
        time_treshold = datetime.now() - timedelta(hours=self.context['time'])
        max_value = sensor.values.filter(
            date_created__gt=time_treshold).aggregate(Max('value'))['value__max']
        max_value_date = sensor.values.filter(
            date_created__gt=time_treshold).filter(value=max_value).order_by('-date_created')
        return max_value_date[0].date_created if max_value_date.__len__() >= 1 else None

    def get_min_value(self, sensor):
        time_treshold = datetime.now() - timedelta(hours=self.context['time'])
        return sensor.values.filter(date_created__gt=time_treshold).aggregate(Min('value'))['value__min']

    def get_min_value_date(self, sensor):
        time_treshold = datetime.now() - timedelta(hours=self.context['time'])
        min_value = sensor.values.filter(
            date_created__gt=time_treshold).aggregate(Min('value'))['value__min']
        min_value_date = sensor.values.filter(
            date_created__gt=time_treshold).filter(value=min_value).order_by('-date_created')
        return min_value_date[0].date_created if min_value_date.__len__() >= 1 else None

    class Meta:
        model = Sensor
        fields = ('index', 'id', 'name', 'display_name',
                  'type', 'show',  'value', 'value_date',  'max_value', 'max_value_date', 'min_value', 'min_value_date')


class DashboardSerializer(serializers.ModelSerializer):
    sensors = DashboardSensorSerializer(many=True)

    class Meta:
        model = Station
        fields = ('index', 'id', 'name', 'display_name',
                  'delay_time', 'show', 'date_created', 'sensors')
