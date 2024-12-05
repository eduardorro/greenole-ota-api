from django.db import models

# Create your models here.

class Device(models.Model):
    identifier = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    version = models.ForeignKey('version.Version', models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.identifier}::{self.name}"
    
    def get_out_topic(self):
        return f'greenole/bk/out/control/{self.identifier}'
    
    def get_ack_topic(self):
        return f'greenole/bk/ack/control/{self.identifier}'