import os
from typing import List
from decorators import register_tool

@register_tool(tags=["file_operations", "read"])
def list_project_files() -> List[str]:
    """Lists all Python files in the current project directory.

    Scans the current directory and returns a sorted list of all files
    that end with '.py'.

    Returns:
        A sorted list of Python filenames
    """
    return sorted([file for file in os.listdir(".")
                    if file.endswith(".py")])

@register_tool(tags=["file_operations", "read"])
def read_file(file_name: str) -> str:
    """Reads and returns the content of a specified project file.

    Opens the file in read mode and returns its entire contents as a string.
    Raises FileNotFoundError if the file doesn't exist.

    Args:
        name: The name of the file to read

    Returns:
        The contents of the file as a string
    """
    with open(file_name, 'r') as f:
        return f.read()

@register_tool(tags=["file_operations", "write"])
def write_file(file_name: str, message: str):
    """Writes a message to a specified file.

    Args:
        file_name: The name of the file to write to
        message: The message to write to the file

    Returns:
        The message as string
    """
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(message)
    except Exception as e:
        print(f"Erro ao criar o arquivo: {e}")
    return message

@register_tool(tags=["system"], terminal=True)
def terminate(message: str):
    """Terminates the agent's execution with a final message.

    Args:
        message: The final message to return before terminating

    Returns:
        The message with a termination note appended
    """
    return message
