from django.db import models

# Create your models here.

class File(models.Model):
    update_script = models.FilePathField()
    target_update = models.FilePathField()
