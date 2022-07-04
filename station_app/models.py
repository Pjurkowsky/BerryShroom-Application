from django.db import models


class Value(models.Model):
    value = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)


class Sensor(models.Model):
    index = models.IntegerField()
    name = models.CharField(max_length=20, default="ERROR", blank=True)
    display_name = models.CharField(max_length=20, default="ERROR", blank=True)
    type = models.CharField(max_length=20, default="ERROR", blank=True)
    show = models.BooleanField(default=True)

    values = models.ManyToManyField(Value, blank=True)

    def __str__(self):
        return self.name


class Station(models.Model):
    index = models.IntegerField()
    name = models.CharField(max_length=20, null=True, blank=True)
    display_name = models.CharField(max_length=20, null=True, blank=True)
    delay_time = models.IntegerField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    show = models.BooleanField(default=True)

    sensors = models.ManyToManyField(Sensor)

    def __str__(self):
        return self.name


class DashboardSettings(models.Model):
    time_last = models.IntegerField()


class ChartSettings(models.Model):
    chart_color = models.CharField(max_length=7, null=True, blank=True)
    min_error_value = models.FloatField()
    max_error_value = models.FloatField()


class Settings(models.Model):
    # dashboard settings
    #card_position = models.IntegerField()
    time_last = models.IntegerField()
    # chart settings
    chart_color = models.CharField(max_length=7, null=True, blank=True)
    min_error_value = models.FloatField()
    max_error_value = models.FloatField()
