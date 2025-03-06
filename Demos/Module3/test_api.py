from src.open_api_client import get_openai_client
from pprint import pprint

client = get_openai_client()
pprint(vars(client))


completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "When was state of Israel founded?"
        }
    ]
)

# Output the response
pprint(completion)
pprint(completion.choices[0].message.content)