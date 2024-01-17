from django.db import models

class Device(models.Model):
    date = models.DateField(auto_now_add = True)
    time = models.TimeField(auto_now_add = True)
    coor = models.TextField()

class Employee(models.Model):
    date = models.DateField(auto_now_add = True)
    time = models.TimeField(auto_now_add = True)
    name = models.TextField()
    sidd = models.TextField()
    pasd = models.TextField()

class Team(models.Model):
    date = models.DateField(auto_now_add = True)
    time = models.TimeField(auto_now_add = True)
    mems = models.ManyToManyField(Employee)