from rest_framework import serializers
from .models import Station, Relay


class RelaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Relay
        fields = ('index', 'id', 'name', 'display_name', 'state', 'mode',
                  't_on', 't_off', 'interval', 'hysteresis', 'set_value', 'sensor_id')

    def create(self, validated_data):
        station = Station.objects.get(index=self.context["station_id"])
        relay = Relay.objects.create(**validated_data)
        relay.save()
        station.relays.add(relay.id)
        return relay

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.display_name = validated_data.get(
            'display_name', instance.display_name)
        instance.state = validated_data.get('state', instance.state)
        instance.mode = validated_data.get('mode', instance.mode)
        instance.t_on = validated_data.get('t_on', instance.t_on)
        instance.t_off = validated_data.get('t_off', instance.t_off)
        instance.interval = validated_data.get('interval', instance.interval)
        instance.set_value = validated_data.get(
            'set_value', instance.set_value)
        instance.sensor_id = validated_data.get(
            'sensor_id', instance.sensor_id)
        instance.save()
        return instance


class StationSerializer(serializers.ModelSerializer):
    relays = RelaySerializer(many=True)

    class Meta:
        model = Station
        fields = ('index', 'id', 'name', 'display_name',
                  'delay_time', 'date_updated', 'relays', )

    def create(self, validated_data):
        relays_data = validated_data.pop('relays')
        station = Station.objects.create(**validated_data)
        station.save()

        for relay_data in relays_data:
            relay = Relay.objects.create(**relay_data)
            station.relays.add(relay.id)
        return station

    def update(self, instance, validated_data):
        relays_data = validated_data.pop('relays')
        instance.name = validated_data.get('name', instance.name)
        instance.display_name = validated_data.get(
            'display_name', instance.display_name)
        instance.delay_time = validated_data.get(
            'delay_time', instance.delay_time)
        instance.save()
        return instance
