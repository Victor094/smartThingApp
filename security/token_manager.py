# token_manager.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class TokenManager:
    def __init__(self):
        # Get the API token from the environment variable
        self.API_TOKEN = os.getenv("API_TOKEN")

    def is_valid_token(self, request_token):
        return request_token == self.API_TOKEN
