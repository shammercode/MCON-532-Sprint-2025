from open_api_client import get_openai_client

def top_p_completion(top_p_value):
    """ Generates AI response with different top_p values to observe variation. """
    messages = [
        {"role": "user", "content": "Give a title for a book about Jewish history."}
    ]

    response = get_openai_client().chat.completions.create(
        model="gpt-3.5-turbo",  # Using the specified model
        messages=messages,
        temperature=0.7,  # Keeps some randomness in choice selection
        top_p=top_p_value  # Adjusts diversity of responses
    )

    print(response.choices[0].message.content)
    print("-" * 80)


def temp_completion(temp_value):
    """ Generates AI response with different top_p values to observe variation. """
    messages = [
        {"role": "user", "content": "Give a title for a book about Jewish history."}
    ]

    response = get_openai_client().chat.completions.create(
        model="gpt-4.0-turbo",  # Using the specified model
        messages=messages,
        temperature=temp_value,  # Keeps some randomness in choice selection  # Adjusts diversity of responses
    )

    print(response.choices[0].message.content)
    print("-" * 80)

def get_title(temp_value):
    messages =[
        {"role": "user", "content": "Give a name for app that helps people to organize their time in the most efficient way."}
    ]


    response = get_openai_client().chat.completions.create(
        model="gpt-3.5-turbo",  # Using the specified model
        messages=messages,
        temperature=temp_value,  # Keeps some randomness in choice selection  # Adjusts diversity of responses
    )

    print(response.choices[0].message.content)
    print("-" * 80)

def main():
    # Running with different top_p values to compare variations
    # for top_p_value in 0.1, .5, .9:
    #     print(f"🔹 Generating Response with top_p={top_p_value}:")
    #     print('-'*80)
    #     for i in range(10):
    #         top_p_completion(top_p_value)  # More focused, deterministic response

    for temp_value in 0.0, 1.0, 1.5:
        print(f"🔹 Generating Response with temperature={temp_value}:")
        print('-'*80)
        for i in range(10):
            get_title(temp_value=temp_value)  # More focused, deterministic response


if __name__ == "__main__":
    main()
