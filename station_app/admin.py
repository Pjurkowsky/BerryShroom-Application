from django.contrib import admin
from .models import Sensor, Station, Value, Settings
admin.site.register(Sensor)
admin.site.register(Station)
admin.site.register(Value)
admin.site.register(Settings)
