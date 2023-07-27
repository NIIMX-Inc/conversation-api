import os
import dotenv
import boto3

from utils.patterns import singleton


# Load environment variables
dotenv.load_dotenv()


@singleton
class SNSClient:
    """Client to connect SNS service."""
    def connect(self):
        return boto3.client(
            'sns',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION_NAME')
        )


@singleton
class SQSClient:
    """Client to connect SQS service."""
    def connect(self):
        return boto3.client(
            'sqs',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION_NAME')
        )


