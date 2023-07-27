import random
import json
from core import process_sns, process_sqs


class Metaverse:
    """Messages management in the metaverse environment."""

    @staticmethod
    def process_sqs_payload(payload):
        """Callback to process SQS payload"""
        message = json.loads(payload['Message'])
        print('IA response: ', message)
    
    def get_responses(self):
        """Pulling IA response from SQS 'Messages' queue."""
        queue_url = 'https://sqs.us-west-1.amazonaws.com/767968023146/Responses'
        process_sqs(queue_url, self.process_sqs_payload)

    @staticmethod
    def send_message(text: str):
        """Send a message to SNS 'Messages' topic to communicate with IA service."""
    
        # Create message object
        conversation_id = random.randint(10000000, 99999999)
        bot_id = random.randint(10000000, 99999999)
        message = {
            "conversation_id": conversation_id,
            "bot_id": bot_id,
            "message": text
        }
        # Send message
        print('Metaverse message: ', message['message'])
        arn = 'arn:aws:sns:us-west-1:767968023146:Messages'
        status = process_sns(arn, message)
        print('Status: ', status)
