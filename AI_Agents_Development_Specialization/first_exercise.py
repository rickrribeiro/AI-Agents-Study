from dotenv import load_dotenv
from litellm import completion

load_dotenv()

def generate_response(messages):
    response = completion(
        model="gemini/gemini-3-flash-preview", 
        messages=messages
    )
    return response.choices[0].message.content

def extract_code_block(response: str) -> str:
    """Extract code block from response"""
    if not '```' in response:
        return response

    code_block = response.split('```')[1].strip()
    if code_block.startswith("python"):
        code_block = code_block[6:]

    return code_block

FIRST_PROMPT = """
You are an expert Python developer. Your task is to create a Python function based on the user's description. Dont include any commentary or extra message,
only return the code.
"""

SECOND_PROMPT = """
You are an expert Python developer. Your task is to add comprehensive documentation to the Python function sended by the user.
Important Rules:
    - Only return the code with the documentation added.
    - Do not include any commentary or extra message.
    - The documentation must include:
Function description
Parameter descriptions
Return value description
Example usage
Edge cases
"""

THIRD_PROMPT = """
You are an expert Python developer. Your task is to create test cases using Python's unittest framework to the documented Python function the user will send to you.
Important Rules:
    - Only return the unitest code.
    Tests should cover:
        Basic functionality
        Edge cases
        Error cases
        Various input scenarios
"""


user_idea = input("Describe the function you want to create: ")

messages = [
        {"role": "system", "content": FIRST_PROMPT},
        {"role": "user", "content": user_idea},
    ]

code_function = generate_response(messages)
code_function = extract_code_block(code_function)
print("--------- FUNCTION CODE ---------")
print(code_function)

messages = [
        {"role": "system", "content": SECOND_PROMPT},
        {"role": "user", "content": code_function},
    ]

documented_code = generate_response(messages)
documented_code = extract_code_block(documented_code)
print("--------- DOCUMENTED CODE ---------")
print(documented_code)

messages = [
        {"role": "system", "content": THIRD_PROMPT},
        {"role": "user", "content": documented_code},
    ]

unit_tests_code = generate_response(messages)
unit_tests_code = extract_code_block(unit_tests_code)
print("--------- UNIT TESTS CODE ---------")
print(unit_tests_code)


with open("function.py", "w", encoding="utf-8") as f:
    f.write(code_function)

with open("documented_function.py", "w", encoding="utf-8") as f:
    f.write(documented_code)

with open("unit_tests.py", "w", encoding="utf-8") as f:
    f.write(unit_tests_code)