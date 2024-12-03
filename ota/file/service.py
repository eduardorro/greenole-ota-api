
from django.conf import settings
import boto3

def _upload_s3(filename, f):
    aws_access_key_id = settings.ACCESS_KEY_ID
    aws_secret_access_key = settings.SECRET_ACCESS_KEY
    bucket_name = settings.OTA_BUCKET

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    transfer_config = boto3.s3.transfer.TransferConfig(
        multipart_threshold=8 * 1024 * 1024,  # 8 MB
        multipart_chunksize=8 * 1024 * 1024,  # 8 MB
    )
    
    s3.upload_fileobj(
        Fileobj=f,
        Bucket=bucket_name,
        Key=filename,
        Config=transfer_config,
        ExtraArgs={'ACL':'public-read'}
    )    

    return f'https://{bucket_name}.s3.amazonaws.com/{filename}'

UPDATE_SCRIPT_FILE = 'update_script_file'
TARGET_UPDATE_FILE = 'target_update_file'

class FileService:
    
    def __init__(self, file, **kwargs) -> None:
        if UPDATE_SCRIPT_FILE  not in kwargs:
            raise ValueError("missing UPDATE_SCRIPT_FILE")
        
        if TARGET_UPDATE_FILE not in kwargs:
            raise ValueError("missing TARGET_UPDATE_FILE")
        
        self.target_update_file = kwargs.get(TARGET_UPDATE_FILE)
        self.update_script_file = kwargs.get(UPDATE_SCRIPT_FILE)
        self.file = file

    def upload_s3(self):
        filename = self.target_update_file.name
        f = self.target_update_file.read()
        target_update_file_link = _upload_s3(filename, f)

        filename = self.update_script_file.name
        f = self.update_script_file.read()
        update_script_file_link = _upload_s3(filename, f)
        
        return update_script_file_link, target_update_file_link

    def save(self):
        update_script_file_link, target_update_file_link = self.upload_s3()
        self.file.update_script_file = update_script_file_link
        self.file.target_update_file_link = target_update_file_link
        self.file.save()
        

