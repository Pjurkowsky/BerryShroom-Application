from django.db import models


class Relay(models.Model):
    MODES = [('MANUAL', 'MANUAL'), ('AUTO', 'AUTO'), ('SENSOR', 'SENSOR'),
             ('TIME_1', 'TIME_1'), ('TIME_2', 'TIME_2')]

    index = models.IntegerField()
    name = models.CharField(max_length=20, null=True, blank=True)
    display_name = models.CharField(max_length=20, null=True, blank=True)
    state = models.BooleanField(default=False)
    mode = models.CharField(max_length=6, choices=MODES, default='MANUAL')
    t_on = models.CharField(max_length=9, default="00:00:00")
    t_off = models.CharField(max_length=9, default="00:00:00")
    interval = models.IntegerField(default=0)
    hysteresis = models.IntegerField(default=0)
    set_value = models.IntegerField(default=0)
    sensor_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Station(models.Model):
    index = models.IntegerField()
    name = models.CharField(max_length=20, null=True, blank=True)
    display_name = models.CharField(max_length=20, null=True, blank=True)
    delay_time = models.IntegerField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    relays = models.ManyToManyField(Relay)

    def __str__(self):
        return self.name
