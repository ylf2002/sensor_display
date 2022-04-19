from sensor.models import Sensors
from sensor.serializers import TempSerializer
from rest_framework import generics

from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
class sensors_api(generics.ListCreateAPIView):
    queryset = Sensors.objects.all()
    serializer_class = TempSerializer


def sensors(request):
    data = Sensors.objects.all()
    res = []
    if data:
        for i in data:
            tt = i.captime
            ax = i.accx
            ay = i.accy
            az = i.accz

            mx = i.magx
            my = i.magy
            mz = i.magz

            gx = i.gyrx
            gy = i.gyry
            gz = i.gyrz

            tx = i.longitude
            ty = i.latitude
            res.append([tt.isoformat(), float(ax), float(ay), float(az), float(mx), float(my), float(mz), float(gx),
                        float(gy), float(gz), float(tx), float(ty)])
    return render(request, 'sensors_index.html', locals())


# 给html传送需要的gps数据
def get_sensors(request):
    data = Sensors.objects.all()
    res = []
    if data:
        for i in data:
            tt = i.captime
            ax = i.accx
            ay = i.accy
            az = i.accz

            mx = i.magx
            my = i.magy
            mz = i.magz

            gx = i.gyrx
            gy = i.gyry
            gz = i.gyrz

            tx = i.longitude
            ty = i.latitude

            res.append({"tt": tt.isoformat(), "ax": float(ax), "ay": float(ay), "az": float(az),
                        "mx": float(mx), "my": float(my), "mz": float(mz),
                        "gx": float(gx), "gy": float(gy), "gz": float(gz),
                        "longitude": float(tx), "latitude": float(ty)})
    return JsonResponse({'s1': res})
