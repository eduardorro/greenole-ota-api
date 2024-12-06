from utils.upload import upload_s3 as _upload_s3


UPDATE_SCRIPT_FILE = 'update_script_file'
TARGET_UPDATE_FILE = 'target_update_file'

class FileService:
    
    def __init__(self, file, **kwargs) -> None:
        if UPDATE_SCRIPT_FILE  not in kwargs:
            raise ValueError("missing UPDATE_SCRIPT_FILE")
        
        if TARGET_UPDATE_FILE not in kwargs:
            raise ValueError("missing TARGET_UPDATE_FILE")
        
        data = kwargs.get(TARGET_UPDATE_FILE)
        if len(data) == 1:
            self.target_update_file = data[0]

        data = kwargs.get(UPDATE_SCRIPT_FILE)
        if len(data) == 1:
            self.update_script_file = data[0]
        
        self.file = file

    def upload_files(self):
        filename = f"files/{self.target_update_file.name}"
        target_update_file_link = _upload_s3(filename, self.target_update_file)

        filename = f"files/{self.update_script_file.name}"
        update_script_file_link = _upload_s3(filename, self.update_script_file)
        
        return update_script_file_link, target_update_file_link

    def save(self):
        self.file.save()
        update_script_file_link, target_update_file_link = self.upload_files()
        self.file.update_script_url = update_script_file_link
        self.file.target_update_url = target_update_file_link
        self.file.save(update_fields=['target_update_url', 'update_script_url'])
        