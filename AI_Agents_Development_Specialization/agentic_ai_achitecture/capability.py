class Capability:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def init(self, agent, action_context: ActionContext) -> dict:
        """Called once when the agent starts running."""
        pass

    def start_agent_loop(self, agent, action_context: ActionContext) -> bool:
        """Called at the start of each iteration through the agent loop."""
        return True

    def process_prompt(self, agent, action_context: ActionContext, 
                      prompt: Prompt) -> Prompt:
        """Called right before the prompt is sent to the LLM."""
        return prompt

    def process_response(self, agent, action_context: ActionContext, 
                        response: str) -> str:
        """Called after getting a response from the LLM."""
        return response

    def process_action(self, agent, action_context: ActionContext, 
                      action: dict) -> dict:
        """Called after parsing the response into an action."""
        return action

    def process_result(self, agent, action_context: ActionContext,
                      response: str, action_def: Action,
                      action: dict, result: any) -> any:
        """Called after executing the action."""
        return result

    def process_new_memories(self, agent, action_context: ActionContext,
                           memory: Memory, response, result,
                           memories: List[dict]) -> List[dict]:
        """Called when new memories are being added."""
        return memories

    def end_agent_loop(self, agent, action_context: ActionContext):
        """Called at the end of each iteration through the agent loop."""
        pass

    def should_terminate(self, agent, action_context: ActionContext,
                        response: str) -> bool:
        """Called to check if the agent should stop running."""
        return False

    def terminate(self, agent, action_context: ActionContext) -> dict:
        """Called when the agent is shutting down."""
        pass


from datetime import datetime
from zoneinfo import ZoneInfo

class TimeAwareCapability(Capability):
    def __init__(self):
        super().__init__(
            name="Time Awareness",
            description="Allows the agent to be aware of time"
        )
        
    def init(self, agent, action_context: ActionContext) -> dict:
        """Set up time awareness at the start of agent execution."""
        # Get timezone from context or use default
        time_zone_name = action_context.get("time_zone", "America/Chicago")
        timezone = ZoneInfo(time_zone_name)
        
        # Get current time in specified timezone
        current_time = datetime.now(timezone)
        
        # Format time in both machine and human-readable formats
        iso_time = current_time.strftime("%Y-%m-%dT%H:%M:%S%z")
        human_time = current_time.strftime("%H:%M %A, %B %d, %Y")
        
        # Store time information in memory
        memory = action_context.get_memory()
        memory.add_memory({
            "type": "system",
            "content": f"""Right now, it is {human_time} (ISO: {iso_time}).
            You are in the {time_zone_name} timezone.
            Please consider the day/time, if relevant, when responding."""
        })
        
    def process_prompt(self, agent, action_context: ActionContext, 
                      prompt: Prompt) -> Prompt:
        """Update time information in each prompt."""
        time_zone_name = action_context.get("time_zone", "America/Chicago")
        current_time = datetime.now(ZoneInfo(time_zone_name))
        
        # Add current time to system message
        system_msg = (f"Current time: "
                     f"{current_time.strftime('%H:%M %A, %B %d, %Y')} "
                     f"({time_zone_name})\n\n")
        
        # Add to existing system message or create new one
        messages = prompt.messages
        if messages and messages[0]["role"] == "system":
            messages[0]["content"] = system_msg + messages[0]["content"]
        else:
            messages.insert(0, {
                "role": "system",
                "content": system_msg
            })
            
        return Prompt(messages=messages)


##########################################################################
@register_tool(tags=["planning"])
def create_plan(action_context: ActionContext,
                memory: Memory,
                action_registry: ActionRegistry) -> str:
   """Create a detailed execution plan based on the task and available tools."""

   # Get tool descriptions for the prompt
   tool_descriptions = "\n".join(
      f"- {action.name}: {action.description}"
      for action in action_registry.get_actions()
   )

   # Get relevant memory content
   memory_content = "\n".join(
      f"{m['type']}: {m['content']}"
      for m in _memory.items
      if m['type'] in ['user', 'system']
   )

   # Construct the prompt as a string
   prompt = f"""Given the task in memory and the available tools, create a detailed plan.
Think through this step by step:

1. First, identify the key components of the task
2. Consider what tools you have available
3. Break down the task into logical steps
4. For each step, specify:
   - What needs to be done
   - What tool(s) will be used
   - What information is needed
   - What the expected outcome is

Write your plan in clear, numbered steps. Each step should be specific and actionable.

Available tools:
{tool_descriptions}

Task context from memory:
{memory_content}

Create a plan that accomplishes this task effectively."""

   return prompt_llm(action_context=action_context, prompt=prompt)


class PlanFirstCapability(Capability):
    def __init__(self, plan_memory_type="system", track_progress=False):
        super().__init__(
            name="Plan First Capability",
            description="The Agent will always create a plan and add it to memory"
        )
        self.plan_memory_type = plan_memory_type
        self.first_call = True
        self.track_progress = track_progress

    def init(self, agent, action_context):
        if self.first_call:
            self.first_call = False
            plan = create_plan(
                action_context=action_context,
                memory=action_context.get_memory(),
                action_registry=action_context.get_action_registry()
            )

            action_context.get_memory().add_memory({
                "type": self.plan_memory_type,
                "content": "You must follow these instructions carefully to complete the task:\n" + plan
            })


##########################################################################
@register_tool(tags=["prompts"])
def track_progress(action_context: ActionContext,
                   _memory: Memory,
                   action_registry: ActionRegistry) -> str:
    """Generate a progress report based on the current task, available tools, and memory context."""

    # Get tool descriptions for the prompt
    tool_descriptions = "\n".join(
        f"- {action.name}: {action.description}"
        for action in action_registry.get_actions()
    )

    # Get relevant memory content
    memory_content = "\n".join(
        f"{m['type']}: {m['content']}"
        for m in _memory.items
        if m['type'] in ['user', 'system']
    )

    # Construct the prompt as a string
    prompt = f"""Given the current task and available tools, generate a progress report.
Think through this step by step:

1. Identify the key components of the task and the intended outcome.
2. Assess the progress made so far based on available information.
3. Identify any blockers or issues preventing completion.
4. Suggest the next steps to move forward efficiently.
5. Recommend any tool usage that might help complete the task.

Write your progress report in clear, structured points.

Available tools:
{tool_descriptions}

Task context from memory:
{memory_content}

Provide a well-organized report on the current progress and next steps."""

    return prompt_llm(action_context=action_context, prompt=prompt)


class ProgressTrackingCapability(Capability):
    def __init__(self, memory_type="system", track_frequency=1):
        super().__init__(
            name="Progress Tracking",
            description="Tracks progress and enables reflection after actions"
        )
        self.memory_type = memory_type
        self.track_frequency = track_frequency
        self.iteration_count = 0

    def end_agent_loop(self, agent, action_context: ActionContext):
        """Generate and store progress report at the end of each iteration."""
        self.iteration_count += 1
        
        # Only track progress on specified iterations
        if self.iteration_count % self.track_frequency != 0:
            return
            
        # Get the memory and action registry from context
        memory = action_context.get_memory()
        action_registry = action_context.get_action_registry()
        
        # Generate progress report
        progress_report = track_progress(
            action_context=action_context,
            _memory=memory,
            action_registry=action_registry
        )
        
        # Add the progress report to memory
        memory.add_memory({
            "type": self.memory_type,
            "content": f"Progress Report (Iteration {self.iteration_count}):\n{progress_report}"
        })