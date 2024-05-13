import os
import boto3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("credentials.env")

# Get AWS credentials and bucket name from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
bucket_name = 'lbs-team-2'
# Configure AWS S3 client
def get_s3_client():
    session = boto3.session.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    return session.client('s3', region_name='eu-west-1')


def upload_to_s3(file_name, bucket, object_name=None):
    """
    Uploads a file to a dedicated folder in an AWS S3 bucket.
    """
    s3_client = get_s3_client()
    response = s3_client.upload_file(file_name, bucket, object_name)
    print(f'Uploaded {file_name} to s3://{bucket}/{object_name}')
    return response


def list_files_in_folder(bucket, folder):
    """
    Lists all files in a folder inside an AWS S3 bucket.
    """
    s3_client = get_s3_client()
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=folder)
    files = [obj['Key'] for obj in response.get('Contents', [])]
    return files


def get_temporary_public_link(bucket, object_name, expiration=3600):
    """
    Retrieves a temporary public link to access an uploaded file in AWS S3.
    """
    s3_client = get_s3_client()
    url = s3_client.generate_presigned_url('get_object',
                                           Params={'Bucket': bucket, 'Key': object_name},
                                           ExpiresIn=expiration)
    return url

# Example usage:
if __name__ == "__main__":
    # Test uploading test.pdf to S3
    file_name = 'test.pdf'
    object_name = 'test pdf'
    upload_to_s3(file_name, bucket_name, object_name)

    # Test listing files in a folder
    folder_name = 'folder/'
    files_in_folder = list_files_in_folder(bucket_name, folder_name)
    print("Files in folder:")
    for file in files_in_folder:
        print(file)

    # Test getting a temporary public link
    public_link = get_temporary_public_link(bucket_name, object_name)
    print("Temporary Public Link:", public_link)
