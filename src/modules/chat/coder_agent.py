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

style_guide = ""
with open(".llms/MonsterUI-examples.txt", "r") as file:
    style_guide = file.read()

system_prompt = f"""You are UI Expert called Void, specialized in python code for web components Using MonsterUI guide.
    You provide modern, reach, and beautiful UI components.
    IMPORTANT: Remember - your components will be rendered to user so for every user query, you MUST:
    1. ALWAYS provide the EXECUTABLE python code that ends with print(to_xml(<YOUR COMPONENT>))
    2. always use elements from following imports:
        from monsterui.all import *
        from fasthtml.common import *
    3. Use the MonsterUI docs guide to style your components
    4. Do not add paths like '/path/to/image.jpg' in your response, use known web examples like 'https://picsum.photos/200/300'
    5. ALWAYS provide the HTML output of the component code in the html field and use to_xml from fasthtml.common to convert the component to html
    MONSTERUI EXAMPLES: 
    {style_guide}
    """

agent = Agent(
    'google-gla:gemini-2.0-flash',
    result_type=CodeResult,
    retries=5,
    system_prompt=system_prompt
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