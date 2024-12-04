from django.conf import settings
import boto3


def upload_s3(filename, f):
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



def copy_s3(src: str, dst: str):    
    aws_access_key_id = settings.ACCESS_KEY_ID
    aws_secret_access_key = settings.SECRET_ACCESS_KEY
    bucket_name = settings.OTA_BUCKET

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    copy_source = {
        'Bucket': bucket_name,
        'Key': src
    }

    s3.meta.client.copy(copy_source, bucket_name, dst)


def delete_all_files_s3(prefix):
    aws_access_key_id = settings.ACCESS_KEY_ID
    aws_secret_access_key = settings.SECRET_ACCESS_KEY
    bucket_name = settings.OTA_BUCKET

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    files_in_folder = response["Contents"]
    files_to_delete = []
    
    for f in files_in_folder:
        files_to_delete.append({"Key": f["Key"]})
    
    s3.delete_objects(
        Bucket=bucket_name, Delete={"Objects": files_to_delete}
    )