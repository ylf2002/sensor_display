from rest_framework import serializers
from sensor.models import Sensors


class TempSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensors
        fields = ['captime', 'accx', 'accy', 'accz', 'magx', 'magy', 'magz', 'gyrx', 'gyry', 'gyrz',
                  'longitude', 'latitude']
