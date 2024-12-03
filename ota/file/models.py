from django.db import models

# Create your models here.

class File(models.Model):
    update_script_file = models.FileField(null=True, blank=True)
    target_update_file = models.FileField(null=True, blank=True)
    update_script_url = models.URLField(null=True, blank=True)
    target_update_url = models.URLField(null=True, blank=True)


