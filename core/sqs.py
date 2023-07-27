import json
from core.client import SNSClient, SQSClient
from typing import Callable


def process_sqs(queue_url: str, callback: Callable):
    """Pulling Metaverse messages from SQS 'Messages' queue."""
    # Set SQS Client to get messages
    sqs = SQSClient().connect()

    while True:
        try:
            # Each message poll lasts 20 seconds
            messages = sqs.receive_message(
                QueueUrl=queue_url,
                AttributeNames=[
                    'SentTimestamp'
                ],
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20
            )
            if 'Messages' in messages:
                for message in messages['Messages']:
                    # Send payload to callback
                    payload = json.loads(message['Body'])
                    callback(payload=payload)      
                    # Delete message
                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=message['ReceiptHandle']
                    )
        except Exception as e:
            print('SQS IA Error:', e)
            raise ValueError('Unable to connect to SQS')
        