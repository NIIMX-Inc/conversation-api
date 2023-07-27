import json
from .client import SNSClient, SQSClient


def process_sns(arn: str, payload: dict):
    """Send a message to SNS 'Messages' topic to communicate with IA service."""
    try:
        # Set SNS client and publish message
        sns = SNSClient().connect()
        response = sns.publish(
            TopicArn=arn,
            Message=json.dumps(payload),
            Subject='Message',
        )

        return response['ResponseMetadata']['HTTPStatusCode']
    except Exception as e:
        print('Send error', e)
