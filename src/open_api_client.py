import os
from openai import OpenAI
from dotenv import load_dotenv

# Load the .env file only once
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

# Initialize the client only once
_client_instance = None

def get_openai_client():
    global _client_instance
    if _client_instance is None:
        api_key = os.getenv("OPENAI_API_KEY")
        org_id = os.getenv("OPENAI_ORG_ID").strip()
        _client_instance = OpenAI(api_key=api_key, organization=org_id)
    return _client_instance
