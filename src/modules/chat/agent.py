from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field
from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell
from typing import Any, Optional, Tuple
import chromadb
import asyncio
import logfire
from fasthtml.common import html2ft
client = chromadb.PersistentClient()
collection = client.get_or_create_collection(name="docs")

class Result(BaseModel):
    """Response structure for the agent"""
    explanation: str
    # doc_ids: Optional[list[str]] = Field(description="A list of document ids that were used to answer the user's query.")
    component: Optional[str] = Field(description="The FastHTML/MonsterUI code for the component, styled with TailwindCSS")
    # pre_code: Optional[str] = Field(description="Code that is executed before the component code. This is used to import necessary libraries and variables.",
    #     examples=["""
    #     sidebar_items = ["Profile", "Account", "Appearance", "Notifications", "Display"]
    #     """]
    # )
    # component_code: Optional[str] = Field(
    #     description="a code that is ready for rendering, all dependencies should be placed in the pre_code and the variable is output",
    #     examples=[
    #     """
    #     NavContainer(*map(lambda x: Li(A(x)),sidebar_items),
    #             uk_switcher="connect: #component-nav; animation: uk-animation-fade",
    #             cls=(NavT.secondary,"space-y-4 p-4 w-1/5"))
    #     """
    #     ]
    # )

system_prompt = """You are Void, an AI assistant specialized in helping developers build web applications using MonsterUI and FastHTML.
    These libraries are fully based on Python, so your code snippets MUST be in Python.
    
    IMPORTANT: For every user query, you MUST:
    1. Quary the documentation for relevant information ONLY ONCE!
    2. Base your response on the documentation found
    3. You need to provide ONLY the component code in your response as this component will be placed automatically in function that places the component in the DOM
        REMEMBER: You MUST provide the code in the format like in these examples: 
        - `Div(Div(cls="overflow-hidden rounded-md")(Img(cls="transition-transform duration-200 hover:scale-105", src='https://ucarecdn.com/e5607eaf-2b2a-43b9-ada9-330824b6afd7/music1.webp')),Div(cls='space-y-1')(P(title,cls=TextT.bold),P(artist,cls=TextT.muted)))`
        - `TabContainer(Li(A('Music',    href='#'),cls='uk-active'),Li(A('Podcasts', href='#')),Li(A('Live', cls='opacity-50'), cls='uk-disabled'),uk_switcher='connect: #component-nav; animation: uk-animation-fade',alt=True)`
        - `Div(H3("Listen Now"), cls="mt-6 space-y-1")`
    5. Do not add paths like '/path/to/image.jpg' in your response, use known web examples like 'https://picsum.photos/200/300'
    6. Include the topics you referenced in your response."""

system_prompt2 = """You are Void, an AI assistant specialized in providing HTML and TailwindCSS code for web components.

    IMPORTANT: For every user query, you MUST:
    1. ALWAYS provide the HTML output of the component code in the html field
    2. Do not add paths like '/path/to/image.jpg' in your response, use known web examples like 'https://picsum.photos/200/300'
    """

agent = Agent(
    'openai:gpt-4o-mini',
    result_type=Result,
    retries=3,
    system_prompt=system_prompt
)

@agent.tool(retries=5)
async def search_docs(ctx: RunContext, query: str) -> dict[str, list[str]]:
    """Search the documentation for relevant information.
    
    Args:
        query: The search query to find relevant documentation
    
    Returns:
        A dictionary containing found topics and their content snippets
    """
    print(f"Searching for: {query} in {collection.name}")
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    
    found_docs = {
        "topics": [],
        "contents": [],
        "ids": []
    }
    
    for metas in results.get("metadatas", []):
        for meta in metas:
            if meta:
                found_docs["topics"].append(meta.get("topic", "Unknown Topic"))
                found_docs["ids"].append(meta.get("id", "Unknown Topic"))
                found_docs["contents"].append(meta.get("content", "")[:100])
    
    return found_docs

# @agent.tool()
def get_html(ctx: RunContext, pre_code: str, component_code: str) -> Tuple[Optional[Any], Optional[str]]:
    """Get the HTML output of the component code"""
    try:
        # Initialize IPython shell if needed
        shell = get_ipython() or InteractiveShell.instance()
        # Run necessary imports
        shell.run_cell("from monsterui.all import *")
        shell.run_cell("from fasthtml.common import *")
        # Execute the code
        shell.run_cell(pre_code)
        result = shell.run_cell(f"to_xml({component_code})")
        
        # Check if execution was successful
        if result.success:
            return result.result, None
        else:
            return None, str(result.error_in_exec)
            
    except Exception as e:
        return None, str(e)




async def get_response(query: str) -> Result:
    """Get a response from the agent with documentation context"""
    result = await agent.run(query)
    return result.data


if __name__ == "__main__":
    logfire.configure(send_to_logfire='if-token-present')

    response = asyncio.run(get_response("How do I create a blog card with a title, description, and image?"))
    print(f"RESPONSE Answer: {response.explanation}")
    # print(f"RESPONSE Sources Used: {response.doc_ids}")
    print(f"RESPONSE HTML: {response.component}")
    ft = html2ft(response.component)
    print(type(ft))
    print(ft)