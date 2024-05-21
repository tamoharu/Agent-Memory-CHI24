import os
import httpx
import dotenv

class Request:
    def __init__(self):
        dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../config/.env'))
        dotenv.load_dotenv(dotenv_path)
        self.api_key = os.getenv('OPENAI_API_KEY')
    
    def agent(self, messages: list) -> str:
        response = httpx.Client(timeout=1000).post(
            'https://api.openai.com/v1/chat/completions',
            json={
                'model': 'gpt-4o',
                'temperature': 0.7,
                'top_p': 1,
                'messages': messages
            },
            headers={'Authorization': f'Bearer {self.api_key}'}
        )
        result = response.json()
        return result['choices'][0]['message']['content']

    def embed(self, document: str):
        response = httpx.Client(timeout=1000).post(
            'https://api.openai.com/v1/embeddings',
            json={
                'model': 'text-embedding-3-small',
                'input': document
            },
            headers={'Authorization': f'Bearer {self.api_key}'}
        )
        result = response.json()
        return result['data'][0]['embedding']