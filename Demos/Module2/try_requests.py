import requests

ERROR_MESSAGE_NEGATIVE = "The number is negative"
ERROR_MESSAGE_ZERO = "The number is zero"

message = "I am trying 'single' quotes"
print(message)
url = 'https://jsonplaceholder.typicode.com/postsit/1'
response = requests.get(url)
print(response.status_code)  # Status code (200 means success)
print(response.json())
message='https://jsonplaceholder.typicode.com/postsit/1'