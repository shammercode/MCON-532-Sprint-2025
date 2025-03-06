import os
from openai import OpenAI
from dotenv import load_dotenv

# Load the .env file only once
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')  #os is a module, path is a method and join allows you to create a path out of 2 paths.
load_dotenv(dotenv_path=dotenv_path)  #then load this, making the stuff in the .env file available

# Initialize the client only once
_client_instance = None

def get_openai_client():
    global _client_instance #creates a global instance of the client for the specific process-be very careful and sparing when doing stuff like this
    if _client_instance is None:
        api_key = os.getenv("OPENAI_API_KEY")
        org_id = os.getenv("OPENAI_ORG_ID").strip()
        _client_instance = OpenAI(api_key=api_key, organization=org_id)
    return _client_instance