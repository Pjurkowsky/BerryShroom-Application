from django.contrib import admin
from .models import DashboardSetting, ChartSetting, Group

admin.site.register(Group)
admin.site.register(DashboardSetting)
admin.site.register(ChartSetting)
