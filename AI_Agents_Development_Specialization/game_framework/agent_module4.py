import json

from core import Agent, AgentFunctionCallingActionLanguage, Environment, Goal, Prompt, PythonActionRegistry
from dotenv import load_dotenv
from litellm import completion
import decorators
import tools

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

    # A read only agent
    agent_language = AgentFunctionCallingActionLanguage()
    read_only_agent = Agent(
        goals=goals,
        agent_language=agent_language,
        action_registry=PythonActionRegistry(tags=["read", "system"]),
        generate_response=generate_response,
        environment=Environment()
    )
    # A full agent
    agent_language = AgentFunctionCallingActionLanguage()
    full_agent = Agent(
        goals=goals,
        agent_language=agent_language,
        action_registry=PythonActionRegistry(tags=["file_operations", "system"]),
        generate_response=generate_response,
        environment=Environment()
    )

    # Run the agent
    print(decorators.tools.keys())
    agent_selection = input("Do you want a read_only_agent or a full_agent?: ")
    user_input = "Write a README for this project."
    if agent_selection == "read_only_agent":
        final_memory = read_only_agent.run(user_input)
    elif agent_selection == "full_agent":
        final_memory = full_agent.run(user_input)
    else:
        print("Invalid input. Please enter 'read_only_agent' or 'full_agent'.")
        return

    # Print the final conversation if desired
    for item in final_memory.get_memories():
        print(f"\n{item['type'].upper()}: {item['content']}")

if __name__ == "__main__":
    main()

