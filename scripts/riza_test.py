from rizaio import Riza
from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic import BaseModel, Field
from typing import Optional
import asyncio

client = Riza()


class HTMLResult(BaseModel):
    """Response structure for the agent"""
    explanation: str
    component_code: Optional[str] = Field(description="The Python FastHTML/MonsterUI code for the component")
    html: Optional[str] = Field(description="The HTML output of the component code")

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
    result_type=HTMLResult,
    retries=5,
    system_prompt=system_prompt
)


@agent.tool()
def execute_code(ctx: RunContext, code: str) -> str:
    """Execute Python code
    Use to_xml from fasthtml.common to convert the component to html of your code and print it to stdout.
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
            "Code executed successfully but produced no output. "
            "Ensure your code includes print statements to get output."
        )

    print(f"Execution output:\n```\n{result.stdout}\n```")
    return result.stdout

if __name__ == "__main__":
    usr_msg = "Please introduce yourself."
    result = agent.run_sync(usr_msg)
    while usr_msg != "quit":
        print(f"RESPONSE Answer: {result.data.explanation}")
        print(f"RESPONSE HTML: {result.data.html}")
        print(f"RESPONSE CODE: {result.data.component_code}")
        usr_msg = input("> ")
        result = agent.run_sync(usr_msg, message_history=result.all_messages())

code = """
from monsterui.all import *
from fasthtml.common import *


def BlogCard(title, author, image_url, content):
    card = Card(
        Div(
            Img(src=image_url, cls="rounded-md w-full", style="object-fit: cover; height: 200px;"),
            Div(
                H3(title, cls="text-lg font-semibold mt-2"),
                P(content, cls="text-sm text-gray-600 mt-1"),
                DivFullySpaced(
                    P(f"By {author}", cls="text-xs text-gray-500"),
                    Button("Read More", cls=ButtonT.secondary),
                    cls="mt-3"
                )
            ),        cls="space-y-2"
        )
    )
    return card

image = "https://picsum.photos/id/237/400/300"

card = BlogCard("The Wonders of AI", "Jane Doe", image, "A captivating exploration into the world of artificial intelligence and its impact on society. This blog post delves into the fascinating world of AI, examining its potential benefits and challenges.")

print(to_xml(card))
"""

# riza = Riza()
# result = riza.command.exec(
#     runtime_revision_id="01JKKHFF03HMX87KZ4XMEEM0Q3",
#     language="python", code=code, http={"allow": [{"host": "*"}]}
# )

# if result.exit_code != 0:
#     print(f"Error message:\n```\n{result.stderr}\n```")
#     raise ModelRetry(result.stderr)
# if result.stdout == "":
#     print(f"Execution output is empty")
#     raise ModelRetry(
#         "Code executed successfully but produced no output. "
#         "Ensure your code includes print statements to get output."
#     )

# print(f"Execution output:\n```\n{result.stdout}\n```")