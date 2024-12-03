from django.db import models

# Create your models here.


class Version(models.Model):
    identifier = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    files = models.ManyToManyField('file.File')