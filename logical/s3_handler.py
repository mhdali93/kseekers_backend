import boto3
import logging
import config
from botocore.exceptions import ClientError
from models.exceptions import AWSConnectionException, AWSS3WriteException, AWSS3PresignedURLException


class S3Handler:
    """Handler for AWS S3 operations like upload and download"""
    
    @staticmethod
    def get_s3_client():
        """Create and return an S3 client"""
        try:
            s3_client = boto3.client(
                's3',
                region_name=config.aws_region,
                aws_access_key_id=config.s3_user_access_key,
                aws_secret_access_key=config.s3_user_access_secret
            )
            return s3_client
        except Exception as e:
            logging.error(f"Error creating S3 client: {e}")
            raise AWSConnectionException(e)

    @staticmethod
    def upload_file(file_path, object_name=None):
        """Upload a file to S3 bucket
        
        Args:
            file_path (str): Path to the file to upload
            object_name (str): S3 object name. If not specified then file_name is used
            
        Returns:
            bool: True if file was uploaded, else False
        """
        # If S3 object_name was not specified, use file_path
        if object_name is None:
            object_name = file_path.split('/')[-1]
            
        try:
            s3_client = S3Handler.get_s3_client()
            s3_client.upload_file(file_path, config.s3_bucket_name, object_name)
            logging.info(f"Successfully uploaded {file_path} to {config.s3_bucket_name}/{object_name}")
            return True
        except ClientError as e:
            logging.error(f"Error uploading file to S3: {e}")
            raise AWSS3WriteException(e)
            
    @staticmethod
    def upload_fileobj(file_obj, object_name):
        """Upload a file-like object to S3 bucket
        
        Args:
            file_obj: File-like object to upload
            object_name (str): S3 object name
            
        Returns:
            bool: True if file was uploaded, else False
        """
        try:
            s3_client = S3Handler.get_s3_client()
            s3_client.upload_fileobj(file_obj, config.s3_bucket_name, object_name)
            logging.info(f"Successfully uploaded file object to {config.s3_bucket_name}/{object_name}")
            return True
        except ClientError as e:
            logging.error(f"Error uploading file object to S3: {e}")
            raise AWSS3WriteException(e)
            
    @staticmethod
    def generate_presigned_url(object_name, expiration=3600):
        """Generate a presigned URL for downloading an S3 object
        
        Args:
            object_name (str): S3 object name
            expiration (int): Expiration time in seconds (default: 1 hour)
            
        Returns:
            str: Presigned URL
        """
        try:
            s3_client = S3Handler.get_s3_client()
            response = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': config.s3_bucket_name, 'Key': object_name},
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            logging.error(f"Error generating presigned URL: {e}")
            raise AWSS3PresignedURLException(e)
            
    @staticmethod
    def delete_object(object_name):
        """Delete an object from S3 bucket
        
        Args:
            object_name (str): S3 object name
            
        Returns:
            bool: True if object was deleted, else False
        """
        try:
            s3_client = S3Handler.get_s3_client()
            s3_client.delete_object(Bucket=config.s3_bucket_name, Key=object_name)
            logging.info(f"Successfully deleted {object_name} from {config.s3_bucket_name}")
            return True
        except ClientError as e:
            logging.error(f"Error deleting object from S3: {e}")
            return False 