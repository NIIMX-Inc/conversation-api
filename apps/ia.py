import json
import os
import dotenv
from core import process_sqs, process_sns
import openai

# Load environment variables
dotenv.load_dotenv()


class IAService:
    """Messages management in the IA environment."""
    @staticmethod
    def create_openai_response(message: str):
        """Process message and generate response."""
        openai.api_key = "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"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "assistant", "content": message}],
            max_tokens=50  # response tokens
        )
        return response

    def process_sqs_payload(self, payload):
        """Callback to process SQS payload"""
        metaverse_payload = json.loads(payload['Message'])
        print('Get Conversation ID:', metaverse_payload['conversation_id'])
        print('Get Message:', metaverse_payload['message'])
        
        #  Logic to process message with model and create metaverse response
        ia_payload = self.create_openai_response(metaverse_payload['message'])
        ia_response = ia_payload['choices'][0]['message']['content']
        ia_response_payload = {**metaverse_payload, 'message': ia_response}

        print('IA Payload', ia_response_payload)

        # Send a response to SNS 'Response' topic to communicate with Metaverse."""
        arn = os.getenv('RESPONSES_ARN_SNS')
        status = process_sns(arn, ia_response_payload)
        print('Status IA Response: ', status)

    def get_messages(self):
        """Pulling Metaverse messages from SQS 'Messages' queue."""
        queue_url = os.getenv('MESSAGES_URL_SQS')
        process_sqs(queue_url, self.process_sqs_payload)
    
