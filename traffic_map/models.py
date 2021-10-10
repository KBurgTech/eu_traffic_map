from django.db import models


# Create your models here.

class RefreshCycle(models.Model):
    finished = models.BooleanField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)


class LiveItem(models.Model):
    refresh_cycle = models.IntegerField()
    loc_latitude = models.FloatField()
    loc_longitude = models.FloatField()
    title = models.CharField(max_length=128)
    type = models.CharField(max_length=16)
    data = models.CharField(max_length=2048)


class RoadAccident(models.Model):
    refresh_cycle = models.IntegerField()
    loc_latitude = models.FloatField()
    loc_longitude = models.FloatField()
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    created_at = models.DateTimeField()


class Roadwork(models.Model):
    refresh_cycle = models.IntegerField()
    loc_latitude = models.FloatField()
    loc_longitude = models.FloatField()
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    type = models.CharField(max_length=16)
    created_at = models.DateTimeField()
