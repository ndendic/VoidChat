from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic import BaseModel, Field
from typing import Optional
import asyncio
import logfire
from rizaio import Riza


class CodeResult(BaseModel):
    """Response structure for the agent"""
    explanation: str
    python_code: Optional[str] = Field(description="The Python FastHTML/MonsterUI code for the component")
    html_output: Optional[str] = Field(description="The HTML output of the component code")

sp = ""
with open(".llms/monsterui_agent_instructions.md", "r") as file:
    sp = file.read()
with open(".llms/MonsterUI-ctx.txt", "r") as file:
    sp += "FULL MonsterUI DOCUMENTATION:\n\n" + file.read()

agent = Agent(
    'google-gla:gemini-2.0-flash',
    result_type=CodeResult,
    retries=15,
    system_prompt=sp
)


@agent.tool()
def execute_code(ctx: RunContext, code: str) -> str:
    """Execute Python code
    Use to_xml from fasthtml.common to convert the component to html of your code and print it to stdout. 
    Like this:
    print(to_xml(component))
    """

    print(f"Agent wanted to execute this code:\n```\n{code}\n```")

    riza = Riza()
    result = riza.command.exec(
        runtime_revision_id="01JKKHFF03HMX87KZ4XMEEM0Q3",
        language="python", code=code, http={"allow": [{"host": "*"}]}
    )

    if result.exit_code != 0:
        print(f"Error message:\n```\n{result.stderr}\n```")
        raise ModelRetry(result.stderr)
    if result.stdout == "":
        print(f"Execution output is empty")
        raise ModelRetry(
            "Code executed successfully but produced no output."
            "Ensure your code includes print(to_xml(<your component>)) at the end of the code to get output."
        )

    print(f"Execution output:\n```\n{result.stdout}\n```")
    return result.stdout

async def get_response(query: str) -> CodeResult:
    """Get a response from the agent with documentation context"""
    result = await agent.run(query)
    return result.data


# if __name__ == "__main__":
#     logfire.configure(send_to_logfire='if-token-present')

#     response = asyncio.run(get_response("How do I create a blog card with a title, description, and image?"))
#     print(f"RESPONSE Answer: {response.explanation}")
#     # print(f"RESPONSE Sources Used: {response.doc_ids}")
#     print(f"RESPONSE HTML: {response.html_output}")
#     print(f"RESPONSE PYTHON: {response.python_code}")