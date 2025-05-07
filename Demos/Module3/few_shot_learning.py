from open_api_client import get_openai_client


def few_shot_completion():
    messages = [
        {"role": "system", "content": "You are a programming assistant."},
        {"role": "user", "content": "Why does my Python code return 'None' when printing a function call?"},
        {"role": "assistant",
         "content": "@@@ -- Functions in Python return 'None' by default if there is no explicit return statement."},
        {"role": "user", "content": "What is the difference between a list and a tuple in Python?"},
        {"role": "assistant",
         "content": "@@@ -- A list is mutable, meaning it can be modified, while a tuple is immutable and cannot be changed after creation. ---@@@"},
        {"role": "user", "content": "How can I write better Python code"}
    ]

    response = get_openai_client().chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.0,
        top_p=0.0
    )
    print(response.choices[0].message.content)


def direct_request():
    messages = [{"role": "system", "content": "You are a programming assistant."},
                {"role": "user", "content": "How can I write better Python code"}
                ]

    response = get_openai_client().chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.0
    )
    print(response.choices[0].message.content)


def main():
    print('--------------  Simple request------------------------')
    direct_request()
    print('--------------  few_shot request------------------------')
    few_shot_completion()


if __name__ == "__main__":
    main()
