import random
import json
import os
import dotenv
from core import process_sns, process_sqs

# Load environment variables
dotenv.load_dotenv()


class Metaverse:
    """Messages management in the metaverse environment."""

    @staticmethod
    def process_sqs_payload(payload):
        """Callback to process SQS payload"""
        ia_response_payload = json.loads(payload['Message'])
        print('IA response: ', ia_response_payload['message'])
    
    def get_responses(self):
        """Pulling IA response from SQS 'Messages' queue."""
        queue_url = os.getenv('RESPONSES_URL_SQS')
        process_sqs(queue_url, self.process_sqs_payload)

    @staticmethod
    def send_message(text: str):
        """Send a message to SNS 'Messages' topic to communicate with IA service."""
    
        # Create message object
        conversation_id = random.randint(10000000, 99999999)
        bot_id = random.randint(10000000, 99999999)
        message = {
            "conversation_id": str(conversation_id),
            "bot_id": str(bot_id),
            "message": text
        }
        # Send message
        print('Metaverse message: ', message['message'])
        arn = os.getenv('MESSAGES_ARN_SNS')
        status = process_sns(arn, message)
        print('Status: ', status)
