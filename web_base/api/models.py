from django.db import models

class Robot(models.Model):
    date = models.DateField(auto_now_add = True)
    time = models.TimeField(auto_now_add = True)
    lati = models.TextField()
    long = models.TextField()
    perc = models.TextField(null = True, blank = True)
    fpsf = models.TextField(null = True, blank = True)
    f1 = models.TextField(null = True, blank = True)
    f2 = models.TextField(null = True, blank = True)

class Device(models.Model):
    date = models.DateField(auto_now_add = True)
    time = models.TimeField(auto_now_add = True)
    nump = models.TextField()
    pasd = models.TextField()
    urln = models.TextField()
    firs = models.BooleanField()
    lati = models.TextField()
    long = models.TextField()
    plat = models.TextField()