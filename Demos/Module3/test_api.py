from src.open_api_client import get_openai_client
from  pprint import pprint

client = get_openai_client()
pprint(vars(client))

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",  # Use a valid OpenAI model name
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistent"
        },
        {
            "role": "user",
            "content": "When was state of Israel founded?"
        },

    ]
)
pprint(completion)
pprint(completion.choices[0].message.content)
