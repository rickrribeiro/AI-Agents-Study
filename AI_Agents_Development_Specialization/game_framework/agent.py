import json

from core import Action, ActionRegistry, Agent, AgentFunctionCallingActionLanguage, Environment, Goal, Prompt
from tools import list_files, read_file, search_in_file, terminate
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

def generate_response(prompt: Prompt) -> str:

    messages = prompt.messages
    tools = prompt.tools

    result = None
    if not tools:
        response = completion(
            model="gemini/gemini-3-flash-preview",
            messages=messages,
            max_tokens=1024
        )
        result = response.choices[0].message.content
    else:
        response = completion(
            model="gemini/gemini-3-flash-preview",
            messages=messages,
            tools=tools,
            max_tokens=1024
        )
        if response.choices[0].message.tool_calls:
            tool = response.choices[0].message.tool_calls[0]
            result = {
                "tool": tool.function.name,
                "args": json.loads(tool.function.arguments),
            }
            result = json.dumps(result)
        else:
            result = response.choices[0].message.content
    return result

def main():
# Define a simple file management goal
    goals = [
            Goal(
                priority=1, 
                name="Explore Files", 
                description="Explore files in the current directory by listing and reading them"
            ),
            Goal(
                priority=2, 
                name="Terminate", 
                description="Terminate the session when tasks are complete with a helpful summary"
            )
        ]

    # Create and populate the action registry
    action_registry = ActionRegistry()

    action_registry.register(Action(
        name="list_files",
        function=list_files,
        description="Returns a list of files in the directory.",
        parameters={},
        terminal=False
    ))

    action_registry.register(Action(
        name="read_file",
        function=read_file,
        description="Reads the content of a specified file in the directory.",
        parameters={
            "type": "object",
            "properties": {
                "file_name": {"type": "string"}
            },
            "required": ["file_name"]
        },
        terminal=False
    ))

    action_registry.register(Action(
        name="terminate",
        function=terminate,
        description="Terminates the conversation. Writes the README.md file and prints the provided message for the user.",
        parameters={
            "type": "object",
            "properties": {
                "file_name": {"type": "string"},
                "message": {"type": "string"},
            },
            "required": ["file_name", "message"]
        },
        terminal=True
    ))

    # A research agent
    agent_language = AgentFunctionCallingActionLanguage()
    environment = Environment()
    file_explorer_agent = Agent(
        goals=goals,
        agent_language=agent_language,
        action_registry=action_registry,
        generate_response=generate_response,
        environment=environment
    )

    # Run the agent
    user_input = "Write a README for this project."
    final_memory = file_explorer_agent.run(user_input)

    # Print the final conversation if desired
    for item in final_memory.get_memories():
        print(f"\n{item['type'].upper()}: {item['content']}")

if __name__ == "__main__":
    main()