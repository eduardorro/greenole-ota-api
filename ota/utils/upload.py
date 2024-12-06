from django.conf import settings
import boto3

aws_access_key_id = settings.ACCESS_KEY_ID
aws_secret_access_key = settings.SECRET_ACCESS_KEY
bucket_name = settings.OTA_BUCKET


def get_s3_client():
    return boto3.Session(profile_name='greenole-prd').client('s3')

def upload_s3(filename, f):
    s3 = get_s3_client()

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



def copy_s3(src: str, dst: str):    
    s3 = get_s3_client()

    copy_source = {
        'Bucket': bucket_name,
        'Key': src
    }

    s3.copy(copy_source, bucket_name, dst)


def delete_all_files_s3(prefix):
    s3 = get_s3_client()

    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    files_in_folder = response["Contents"] if "Contents" in response else []
    files_to_delete = []
    
    if not files_in_folder:
        return
    
    for f in files_in_folder:
        files_to_delete.append({"Key": f["Key"]})
    
    s3.delete_objects(
        Bucket=bucket_name, Delete={"Objects": files_to_delete}
    )