from django.db import models

# Create your models here.



class VersionUpdate(models.Model):
    SUCCESS = 1
    FAILED = 2
    IN_PROGRESS = 3

    STATUS = (
        ('SUCCESS', SUCCESS),
        ('FAILED', FAILED),
        ('IN_PROGRESS', IN_PROGRESS)
    )

    device = models.ForeignKey('device.Device', models.CASCADE)
    update = models.ForeignKey('update.Update', models.CASCADE)
    version = models.ForeignKey('version.Version', models.CASCADE)
    status = models.IntegerField(choices=STATUS, default=IN_PROGRESS)


class Update(models.Model):
    versions = models.ManyToManyField('device.Device', through=VersionUpdate)


