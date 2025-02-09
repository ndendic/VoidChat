from pydantic_ai import Agent
from pydantic import BaseModel

class TaskResult(BaseModel):
    explanation: str
    result: str

chat_manager = Agent(
    "google-gla:gemini-2.0-flash",
    result_type=TaskResult,
    system_prompt="""
    You are a helpful assistant that can help with a variety of tasks.
    """
)

async def propose_title(message: str):
    result = await chat_manager.run(f"propose the appropriate title of the chat which first message is '{message}'")
    return result.data.result
