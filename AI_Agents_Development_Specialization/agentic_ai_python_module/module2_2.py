import json
from dotenv import load_dotenv
from litellm import completion
import os
import sys
from typing import List, Dict

load_dotenv()

# def generate_response(messages):
#     response = completion(
#         model="gemini/gemini-3-flash-preview", 
#         messages=messages
#     )
#     return response.choices[0].message.content


def list_files() -> List[str]:
    """List files in the current directory."""
    return os.listdir(".")

def read_file(file_name: str) -> str:
    """Read a file's contents."""
    try:
        with open(file_name, "r") as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: {file_name} not found."
    except Exception as e:
        return f"Error: {str(e)}"

tool_functions = {
    "list_files": list_files,
    "read_file": read_file
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Returns a list of files in the directory.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a specified file in the directory.",
            "parameters": {
                "type": "object",
                "properties": {"file_name": {"type": "string"}},
                "required": ["file_name"]
            }
        }
    }
]

# Our rules are simplified since we don't have to worry about getting a specific output format
agent_rules = [{
    "role": "system",
    "content": """
You are an AI agent that can perform tasks by using available tools. 

If a user asks about files, documents, or content, first list the files before reading them.
"""
}]

user_task = input("What would you like me to do? ")

memory = [{"role": "user", "content": user_task}]

messages = agent_rules + memory

response = response = completion(
        model="gemini/gemini-3-flash-preview", 
        messages=messages,
        tools=tools
    )

assistant_message = response.choices[0].message
messages.append(assistant_message)

tool_call = assistant_message.tool_calls[0]
tool_name = tool_call.function.name
tool_args = json.loads(tool_call.function.arguments)
result = tool_functions[tool_name](**tool_args)

messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "name": tool_name,
    "content": str(result)
})

print(f"Tool Name: {tool_name}")
print(f"Tool Arguments: {tool_args}")
print(f"Result: {result}")

final_response = completion(
    model="gemini/gemini-3-flash-preview",
    messages=messages,
    tools=tools
)

print(f"Próximo passo do Gemini: {final_response.choices[0].message.content}")