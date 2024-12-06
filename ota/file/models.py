from django.db import models

class File(models.Model):
    name = models.CharField(max_length=150, default="")
    update_script_file = models.FileField(null=True, blank=True)
    target_update_file = models.FileField(null=True, blank=True)
    update_script_url = models.URLField(null=True, blank=True)
    target_update_url = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    def get_key(self, url):
        return "/".join(url.split("/")[-2:])
    
    def get_update_script_url_key(self):
        return self.get_key(self.update_script_url)
    
    def get_target_update_url_key(self):
        return self.get_key(self.target_update_url)
