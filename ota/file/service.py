from utils.upload import upload_s3 as _upload_s3


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

    def upload_files(self):
        filename = f"files/{self.target_update_file.name}"
        f = self.target_update_file.read()
        target_update_file_link = _upload_s3(filename, f)

        filename = f"files/{self.update_script_file.name}"
        f = self.update_script_file.read()
        update_script_file_link = _upload_s3(filename, f)
        
        return update_script_file_link, target_update_file_link

    def save(self):
        update_script_file_link, target_update_file_link = self.upload_files()
        self.file.update_script_file = update_script_file_link
        self.file.target_update_file_link = target_update_file_link
        self.file.save()
        

