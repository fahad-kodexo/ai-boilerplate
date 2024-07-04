import boto3
import requests
from botocore.config import Config
from typing import Dict

from app.utils.constants import ACCESS_KEY, AWS_REGION, S3_BUCKET_NAME, SECRET_ACCESS_KEY

config = Config(signature_version='s3v4')
s3_client = boto3.client("s3",
                         config=config,
                         aws_secret_access_key = SECRET_ACCESS_KEY,
                         aws_access_key_id = ACCESS_KEY,
                         region_name = AWS_REGION)

class S3:
    EXPIRATION  = 180
    CLIENT_METHOD = 'get_object'
    @staticmethod
    def generate_presigned_url(object_name) -> Dict:
        try:
            return s3_client.generate_presigned_url(
                ClientMethod=S3.CLIENT_METHOD,
                Params={
                    'Bucket': S3_BUCKET_NAME,
                    'Key': object_name
                },
                ExpiresIn=S3.EXPIRATION
            )

        except Exception as e:
            print("Error in generate_presigned_url",e)
            return None

    @staticmethod 
    def generate_presigned_post(object_name, folder_path):
        try:
            s3_response = s3_client.generate_presigned_post(Bucket=S3_BUCKET_NAME,
                                                        Key=folder_path+"/"+object_name,
                                                        ExpiresIn=S3.EXPIRATION)
            
            # Upload the file using requests module
            with open(object_name, 'rb') as f:
                files = {'file': (object_name, f)}
                response = requests.post(s3_response['url'], data=s3_response['fields'], files=files)
            return response.status_code
                        
        except Exception as e:
            print("Error in generate_presigned_post",e)
            return None
