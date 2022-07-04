from django.db import models


class DashboardSetting(models.Model):
    time_last = models.IntegerField(default=24)
    #card_position = models.IntegerField()


class ChartSetting(models.Model):
    chart_color = models.CharField(max_length=7, default="#0000FF")
    min_error_value = models.FloatField(null=True, blank=True)
    max_error_value = models.FloatField(null=True, blank=True)


class Group(models.Model):

    name = models.CharField(max_length=30)
    list_of_indexes = models.CharField(max_length=2000, default="[]")
    dashboard_settings = models.ForeignKey(
        DashboardSetting, blank=True, null=True, on_delete=models.SET_NULL)
    chart_settings = models.ForeignKey(
        ChartSetting, blank=True, null=True, on_delete=models.SET_NULL)
