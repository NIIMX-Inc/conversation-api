import json
import os
import dotenv
from core import process_sqs, process_sns

# Load environment variables
dotenv.load_dotenv()


class IAService:
    """Messages management in the IA environment."""
    @staticmethod
    def process_sqs_payload(payload):
        """Callback to process SQS payload"""
        message = json.loads(payload['Message'])
        print('Get Conversation ID:', message['conversation_id'])
        print('Get Message:', message['message'])
        
        #  Logic to process message with model and create metaverse response
        message['message'] = 'Hi Bryan!'

        # Send a response to SNS 'Response' topic to communicate with Metaverse."""
        arn = os.getenv('RESPONSES_ARN_SNS')
        status = process_sns(arn, message)
        print('Status IA Response: ', status)

    def get_messages(self):
        """Pulling Metaverse messages from SQS 'Messages' queue."""
        queue_url = os.getenv('MESSAGES_URL_SQS')
        process_sqs(queue_url, self.process_sqs_payload)
    
