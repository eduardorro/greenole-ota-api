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

    device = models.ForeignKey('device.Device', models.CASCADE, null=True, blank=True)
    update = models.ForeignKey('update.Update', models.CASCADE, null=True, blank=True)
    status = models.IntegerField(choices=STATUS, default=CREATED)

    def __str__(self):
        return f"{self.update} - Device: {self.device}"


class Update(models.Model):
    name = models.CharField(max_length=150, default="")
    all_devices = models.BooleanField(default=False)
    version = models.ForeignKey('version.Version', models.CASCADE, null=True, blank=True)
    devices = models.ManyToManyField('device.Device', through=VersionUpdate)

    def __str__(self) -> str:
        result = f"{self.name} - Version: {self.version}"
        return result
