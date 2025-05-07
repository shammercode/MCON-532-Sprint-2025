from src.open_api_client import get_openai_client
from  pprint import pprint

def chat_with_gpt(client, system_prompt, user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

# Example System Prompts
system_prompts = [
    "You are a helpful assistant.",
    "You are a strict grammar teacher.",
    "You are a sarcastic AI with a humorous tone.",
    "You are an AI that only responds in rhymes.",
    "You are a middle school teacher"
]

# User Input
user_input = "Explain the importance of version control."

# Execute
if __name__ == "__main__":
    client = get_openai_client()
    for prompt in system_prompts:
        response = chat_with_gpt(client,prompt, user_input)
        print(f"System Prompt: {prompt}\nResponse: {response}\n")