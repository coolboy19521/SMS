from django.db import models

class Museum(models.Model):
    name = models.CharField(max_length = 256)
    address = models.CharField(max_length = 256)
    key = models.CharField(max_length = 256)

class Exhibit(models.Model):
    museum = models.ForeignKey(Museum, on_delete = models.CASCADE)
    name = models.CharField(max_length = 256)
    audio = models.FileField(upload_to = 'static/audios/')
    video = models.FileField(upload_to = 'static/videos/')
    thumbnail = models.FileField(upload_to = 'static/thumbs/', null=True)
    desc = models.TextField(null = True)
