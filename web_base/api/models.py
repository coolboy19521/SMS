from django.db import models

class Robot(models.Model):
    date = models.DateField(auto_now_add = True)
    time = models.TimeField(auto_now_add = True)
    coor = models.TextField()

class Device(models.Model):
    date = models.DateField(auto_now_add = True)
    time = models.TimeField(auto_now_add = True)
    nump = models.TextField()
    pasd = models.TextField()
    urln = models.TextField()
    firs = models.BooleanField()