from django.contrib import admin

# Register your models here.
from .models import *


class SensorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'captime', 'accx', 'accy', 'accz', 'magx', 'magy', 'magz', 'gyrx', 'gyry', 'gyrz',
                    'longitude', 'latitude')


admin.site.register(Sensors, SensorsAdmin)
