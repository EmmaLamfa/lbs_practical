import os
import boto3
from dotenv import load_dotenv
from config import Settings
from fastapi import UploadFile




def get_client(service: str, settings: Settings):
    session = boto3.session.Session(
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key.get_secret_value(),
    )
    return session.client(service, region_name='eu-west-1')


def upload_file_to_s3(s3_client, object_name, bucket_name, file: UploadFile):
    s3_client.upload_fileobj(file.file, bucket_name, object_name)
    return object_name


def list_files(s3_client, bucket_name):
    paginator = s3_client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket_name)

    files = []
    for page in page_iterator:
        for obj in page.get('Contents', []):  # Ensure there are contents
            key = obj['Key']
            if not key.endswith('/'):  # Exclude folders
                files.append(key)
    return files

def generate_presigned_url(bucket_name: str, object_name: str, expiration: int = 3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string, name of the bucket.
    :param object_name: string, name of the object.
    :param expiration: Time in seconds for the presigned URL to remain valid.
    :return: Presigned URL as string. If error, returns None.
    """
    # Create a s3 client
    s3_client = boto3.client('s3')

    return s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': object_name},
        ExpiresIn=expiration)
