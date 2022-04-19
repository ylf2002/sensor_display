from django.conf.urls import url
from sensor import views

urlpatterns = [
    url(r'^$', views.sensors, name='sensor.sensors'),
    url(r'^sensors_api', views.sensors_api.as_view(), name='sensor.sensors_api'),
    url(r'^get_sensors', views.get_sensors, name='sensor.get_sensors'),
]
