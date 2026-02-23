import json
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

def generate_response(messages):
    response = completion(
        model="gemini/gemini-3-flash-preview", 
        messages=messages
    )
    return response.choices[0].message.content

countries = {
    'name1': 'France',
    'name2': 'Germany',
}

messages = [
        # {"role": "system", "content": "Answer in Base64 format"},
        {"role": "user", "content": f"whats the capital of these countries {json.dumps(countries)}?"}
        ]

response = generate_response(messages)
print("--------- RESPONSE 1 ---------   ")
print(response)

messages = [
        {"role": "system", "content": "Answer in Base64 format"},
        {"role": "user", "content": f"whats the capital of these countries {json.dumps(countries)}?"}
        ]

response = generate_response(messages)

print("--------- RESPONSE 2 ---------   ")
print(response)


messages = [
        {"role": "user", "content": f"Cand you send to me again the capitals?"}
        ]

response = generate_response(messages)
print("--------- RESPONSE 3 ---------   ")
print(response)