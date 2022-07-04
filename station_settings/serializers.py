from .models import Group, DashboardSetting, ChartSetting
from rest_framework import serializers
import json


class DashboardSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardSetting
        fields = '__all__'


class ChartSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartSetting
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    dashboard_settings = DashboardSettingSerializer(many=False)
    chart_settings = ChartSettingSerializer(many=False)

    class Meta:
        model = Group
        fields = ('id', 'name', 'list_of_indexes',
                  'dashboard_settings', 'chart_settings')

    def create(self, validated_data):
        dhsettings_data = validated_data.pop('dashboard_settings')
        cssettings_data = validated_data.pop('chart_settings')
        group = Group.objects.create(**validated_data)
        dashboard_settings = DashboardSetting.objects.create(
            group=group, **dhsettings_data)
        chart_settings = ChartSetting.objects.create(
            group=group, **cssettings_data)
        dashboard_settings.group_set.add(group)
        chart_settings.group_set.add(group)
        group.save()
        return group

    def update(self, instance, validated_data):

        dhsettings_data = validated_data.pop('dashboard_settings')
        cssettings_data = validated_data.pop('chart_settings')
        instance.name = validated_data.get('name', instance.name)
        instance.list_of_indexes = validated_data.get(
            'list_of_indexes', instance.list_of_indexes)

        instance.save()

        dashboad_settings = DashboardSetting.objects.get(group=instance)
        dashboad_settings.time_last = dhsettings_data.get(
            'time_last', dashboad_settings.time_last)
        dashboad_settings.save()

        chart_settings = ChartSetting.objects.get(group=instance)
        chart_settings.chart_color = cssettings_data.get(
            'chart_color', chart_settings.chart_color)
        chart_settings.min_error_value = cssettings_data.get(
            'min_error_value', chart_settings.min_error_value)
        chart_settings.max_error_value = cssettings_data.get(
            'max_error_value', chart_settings.max_error_value)
        chart_settings.save()

        return instance

    def validate(self, data):

        sensors = json.loads(data.get('list_of_indexes'))
        # print(sensors)
        for (i, sensorx) in enumerate(sensors):
            for (j, sensory) in enumerate(sensors):
                if i != j and sensorx['station_index'] == sensory['station_index'] and sensorx['sensor_index'] == sensory['sensor_index']:
                    raise serializers.ValidationError('essa')
        allsensors = Group.objects.all()
        for sensorss in allsensors:
            sensorsss = json.loads(sensorss.list_of_indexes)
            # print(sensorsss)
        #     for (i, sensorx) in enumerate(sensorsss):
        #         for (j, sensory) in enumerate(sensors):
        #             if i != j and sensorx['station_index'] == sensory['station_index'] and sensorx['sensor_index'] == sensory['sensor_index']:
        #                 raise serializers.ValidationError('essa')

        return data
