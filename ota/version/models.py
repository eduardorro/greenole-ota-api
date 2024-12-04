from django.db import models

# Create your models here.


class Version(models.Model):
    identifier = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    files = models.ManyToManyField('file.File')
    latest = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"V{self.identifier} - {self.name}"
    
    def get_version(self) -> str:
        return f"{self.name.replace(" ", "_")}/{self.identifier.replace(".", "_")}"