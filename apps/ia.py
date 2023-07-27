import json
from core import process_sqs, process_sns


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
        arn = 'arn:aws:sns:us-west-1:767968023146:Responses'
        status = process_sns(arn, message)
        print('Status IA Response: ', status)

    def get_messages(self):
        """Pulling Metaverse messages from SQS 'Messages' queue."""
        queue_url = 'https://sqs.us-west-1.amazonaws.com/767968023146/Messages'
        process_sqs(queue_url, self.process_sqs_payload)
    
