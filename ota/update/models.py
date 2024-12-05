from django.db import models


class VersionUpdate(models.Model):
    SUCCESS = 1
    FAILED = 2
    IN_PROGRESS = 3
    CREATED = 4

    STATUS = (
        (SUCCESS, 'SUCCESS'),
        (FAILED, 'FAILED'),
        (IN_PROGRESS, 'IN_PROGRESS'),
        (CREATED, 'CREATED'),
    )

    device = models.ForeignKey('device.Device', models.CASCADE)
    update = models.ForeignKey('update.Update', models.CASCADE)
    status = models.IntegerField(choices=STATUS, default=CREATED)


class Update(models.Model):
    name = models.CharField(max_length=150, default="")
    all_devices = models.BooleanField(default=False)
    version = models.ForeignKey('version.Version', models.CASCADE, null=True, blank=True)
    versions = models.ManyToManyField('device.Device', through=VersionUpdate)

    def __str__(self) -> str:
        result = f"{self.name} - Version: {self.version}"
        return result
