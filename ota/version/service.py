from .models import Version
from utils.upload import copy_s3, delete_all_files_s3 as _delete_all_files_s3
from django.conf import settings
import json

BUCKET_NAME = settings.OTA_BUCKET

class VersionService:
    LATEST_PREFIX = 'version/latest'

    def __init__(self, version: Version) -> None:
        self.version = version

    def _get_filename(self, key):
        return key.split("/")[-1]
    
    def copy_files(self, prefix):
        for file in self.version.files.all():
            update_script_key = file.get_update_script_url_key()
            target_update_key = file.get_target_update_url_key()
            
            copy_s3(update_script_key, f"{prefix}/{self._get_filename(update_script_key)}")
            copy_s3(target_update_key, f"{prefix}/{self._get_filename(target_update_key)}")
        
    def save(self):
        self.version.save()
        prefix = self.version.get_version()
        self.delete_all_files_s3(prefix)
        self.copy_files(prefix)
        
    
    def delete_all_files_s3(self, prefix):
        _delete_all_files_s3(prefix)
    
    def make_latest(self):
        prefix = VersionService.LATEST_PREFIX
        self.delete_all_files_s3(prefix)        
        self.copy_files(prefix)
        
        self.version.latest = True
        self.version.save(update_fields=['latest'])

        Version.objects.exclude(id=self.version.id).update(latest=False)

    def get_version_base_url(self):
        if self.version.latest:
            url = f'https://{BUCKET_NAME}.s3.amazonaws.com/{VersionService.LATEST_PREFIX}/'
        else:
            url = f'https://{BUCKET_NAME}.s3.amazonaws.com/{self.version.get_version()}/'

        return url

    def get_all_version_files(self) -> list:
        result = []
        base_url = self.get_version_base_url()
        for file in self.version.files.all():
            for key in [file.get_update_script_url_key(), file.get_target_update_url_key()]:            
                file_name = self._get_filename(key)
                result.append(f"{base_url}{file_name}")

        return result
    
    def get_version_payload(self) -> str:
        url = self.get_version_base_url()
        
        return {
            'url': url,
            'version': str(self.version),
            'files': self.get_all_version_files()
        }
