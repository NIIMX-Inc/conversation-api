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
    def create_aishia_response(message: str):
        """Process message and generate Aishia text response. This function returns a text string."""
        # Example with OpenAI response
        openai.api_key = "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"
        response_payload = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[{"role": "assistant", "content": message}],
            max_tokens=50  # response tokens
        )
        response = response_payload['choices'][0]['message']['content']

        # Generate static response
        # response = f"Hi user! I'm Aishia and your question is {message}"

        return response

    def process_sqs_payload(self, payload):
        """Callback to process SQS payload"""
        metaverse_payload = json.loads(payload['Message'])
        print('Conversation ID:', metaverse_payload['conversation_id'])
        print('Message:', metaverse_payload['message'])
        
        #  Logic to process message with model and create metaverse response
        ia_response = self.create_aishia_response(metaverse_payload['message'])
        ia_response_payload = {**metaverse_payload, 'message': ia_response}
        print('IA response to send:', ia_response_payload)

        # Send a response to SNS 'Response' topic to communicate with Metaverse."""
        arn = os.getenv('RESPONSES_ARN_SNS')
        status = process_sns(arn, ia_response_payload)
        print('Status IA Response: ', status)

    def get_messages(self):
        """Pulling Metaverse messages from SQS 'Messages' queue."""
        queue_url = os.getenv('MESSAGES_URL_SQS')
        process_sqs(queue_url, self.process_sqs_payload)
    
