from .models import Version
from utils.upload import copy_s3, delete_all_files_s3 as _delete_all_files_s3

class VersionService:
    LATEST_PREFIX = 'version/latest/'

    def __init__(self, version: Version) -> None:
        self.version = version


    def _get_filename(self, key):
        return key.split("/")[-1]
    
    def copy_files(self, prefix):
        for file in self.version.files:
            update_script_key = file.get_update_script_url_key()
            target_update_key = file.get_target_update_url_key()
            
            copy_s3(update_script_key, f"{prefix}/{self._get_filename(update_script_key)}")
            copy_s3(target_update_key, f"{prefix}/{self._get_filename(update_script_key)}")
        
    def save(self):
        prefix = self.version.get_version()
        self.delete_all_files_s3(prefix)
        self.copy_files(prefix)
        self.version.save()
    
    def delete_all_files_s3(self, prefix):
        _delete_all_files_s3(prefix)
    
    def make_latest(self):
        prefix = VersionService.LATEST_PREFIX
        self.delete_all_files_s3(prefix)        
        self.copy_files(prefix)
        self.version.latest = True
        self.version.save(update_fields=['latest'])
