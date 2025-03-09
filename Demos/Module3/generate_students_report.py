from openai.types.chat import ChatCompletion
from src.open_api_client import get_openai_client
from pprint import pprint
import os

def ask_gpt(prompt:str)->ChatCompletion:
    """
    Receives a string, and then calls get_openai_client to create an OpenAI API client,
    sending the string in as a prompt, and returning the completion.
    :param prompt: string to send as the content of the prompt
    :return: ChatCompletion from prompt
    """
    client = get_openai_client()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion

def populate_file(file_path: str, contents: str):
    """
    Receives a file path and string and then writes the string to the file.
    :param file_path: string of file path to write to
    :param contents: string to write to file
    """
    with open(file_path, 'w') as file:
        file.write(contents)

def get_and_handle_single_file(file_path: str, prompt: str):
    """
    Receives a file path and a prompt, calls ask_gpt method, passing the prompt.
    It then writes the response into the file using the populate_file method,
    and prints it to the console.
    :param code_file_path: string of file path to write to
    :param prompt: string of prompt to send to gpt model
    """
    response = ask_gpt(prompt)
    populate_file(file_path, response.choices[0].message.content)
    pprint(response.choices[0].message.content)

def get_and_handle_code_with_tests_files(code_file_path: str, tests_file_path: str, prompt: str):
    """
    Receives two file paths and a prompt, calls ask_gpt method, passing the prompt, and then writes
    the response and writes it into the two files using the populate_file method, splitting it by the
    word class and placing the first half in code_file_path and the second in test_file_path. It then
    prints the response in full to the console.
    :param code_file_path: string of file path to write code to
    :param test_file_path: string of file path to write test cases to
    :param prompt: string of prompt to send to gpt model
    """
    response = ask_gpt(prompt)
    pprint(response.choices[0].message.content)
    pieces = response.choices[0].message.content.split("class", 1)
    populate_file(code_file_path, pieces[0])
    populate_file(tests_file_path, "class" + pieces[1])
    pprint(response.choices[0].message.content)

def create_basic_dictionary(file_path: str):
    """
    Receives a file path and calls get_and_handle_single_file method, passing it a prompt to create
    a Python dictionary of student ID to dictionary of name(string), grades(integer),
    gpa((sum of grades / number of grades) / 25, rounded to two decimal places) in the file path passed.
    :param file_path: string of file path to write code to
    """
    prompt = """
    Create a Python dictionary where each student ID maps to another dictionary containing:
    "name": Student’s name (string)
    "grades": A list of grades (integers).
    "gpa": The GPA, calculated as (sum of grades / number of grades) / 25, rounded to two decimal places.
    """
    get_and_handle_single_file(file_path, prompt)
def create_dictionary_with_dictionary_comprehension(file_path: str):
    """
    Receives a file path and calls get_and_handle_single_file method, passing it a prompt to create
    a Python dictionary using dictionary comprehension of student ID to dictionary of name(string),
    grades(integer), gpa((sum of grades / number of grades) / 25, rounded to two decimal places)
    in the file path passed.
    :param file_path: string of file path to write code to
    """
    prompt = """
    Create a Python dictionary where each student ID maps to another dictionary containing:
    "name": Student’s name (string)
    "grades": A list of grades (integers).
    "gpa": The GPA, calculated as (sum of grades / number of grades) / 25, rounded to two decimal places.
    Use dictionary comprehension to construct the dictionary.
    """
    get_and_handle_single_file(file_path, prompt)
def create_dictionary_formatted_for_readability(file_path: str):
    """
    Receives a file path and calls get_and_handle_single_file method, passing it a prompt to create
    a Python dictionary using dictionary comprehension of student ID to dictionary of name(string),
    grades(integer), gpa((sum of grades / number of grades) / 25, rounded to two decimal places) and
    formatted for readability in the file path passed.
    :param file_path: string of file path to write code to
    """
    prompt = """
    Create a Python dictionary where each student ID maps to another dictionary containing:
    "name": Student’s name (string)
    "grades": A list of grades (integers).
    "gpa": The GPA, calculated as (sum of grades / number of grades) / 25, rounded to two decimal places.
    Use dictionary comprehension, and then format the output using print() so that the student data is displayed in a well-structured format.
    """
    get_and_handle_single_file(file_path, prompt)

def create_dictionary_with_dictionary_comprehension_and_tests(code_file_path: str, test_file_path: str):
    """
    Receives two file paths and calls get_amd_handle_code_with_tests_files method, passing it a prompt to create
    a Python dictionary using dictionary comprehension of student ID to dictionary of name(string),
    grades(integer), gpa((sum of grades / number of grades) / 25, rounded to two decimal places) for the code
    file and tests for that code in the second file.
    :param code_file_path: string of file path to write code to
    :param test_file_path: string of file path to write test cases to
    """
    prompt = """
    Create a Python dictionary compatible with Python 3.12 where each student ID maps to another dictionary containing:
    "name": Student’s name (string)
    "grades": A list of grades (integers).
    "gpa": The GPA, calculated as (sum of grades / number of grades) / 25, rounded to two decimal places.
    Use dictionary comprehension to create it.
    Then, write unit tests using unittest to verify that:
    The dictionary contains the correct number of students.
    Each student has a "name", "grades", and "gpa".
    The "grades" list contains only integers.
    Ensure test coverage using IntelliJ’s built-in coverage tool.
    """
    get_and_handle_code_with_tests_files(code_file_path, test_file_path, prompt)
    
def main():
    code_path = os.path.join(os.path.dirname(__file__), 'generated_students.py')#create file path for code
    tests_path = os.path.join(os.path.dirname(__file__), 'test_students.py')#create file path for tests
    #create_basic_dictionary(code_path)
    #create_dictionary_with_dictionary_comprehension(code_path)
    #create_dictionary_formatted_for_readability(code_path)
    create_dictionary_with_dictionary_comprehension_and_tests(code_path, tests_path)

if __name__ == '__main__':
    main()