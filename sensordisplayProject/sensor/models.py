from django.db import models


# Create your models here.
class Sensors(models.Model):
    captime = models.DateTimeField(auto_now_add=False)
    accx = models.CharField(max_length=10)  # 加速度
    accy = models.CharField(max_length=10)
    accz = models.CharField(max_length=10)
    magx = models.CharField(max_length=10)  # 磁力计
    magy = models.CharField(max_length=10)
    magz = models.CharField(max_length=10)
    gyrx = models.CharField(max_length=10)  # 陀螺仪
    gyry = models.CharField(max_length=10)
    gyrz = models.CharField(max_length=10)
    longitude = models.CharField(max_length=10)  # 经度
    latitude = models.CharField(max_length=10)  # 维度
