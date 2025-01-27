import json
import uuid
import subprocess

from config import Settings

from starlette.responses import RedirectResponse
from fasthtml.common import *
from fasthtml.core import APIRouter
from monsterui.all import *
from modules.shared.templates import app_template

from .models import ChatMessage, Chat
from .agent import agent, Result
from uuid import UUID

config = Settings()
rt = APIRouter()
messages = []

def ChatInput():
    return Input(
            id="msg",
            name="msg",
            placeholder="Type your message...",
            cls="flex-1",
            required=True,
            autofocus=True,
            # hx_swap_oob='true'
        )

def chat_section(request, chat):
    return Div(cls="min-h-[calc(100vh-4rem)] flex flex-col" )(
        CardContainer(cls="flex-1 flex flex-col m-4 max-h-[calc(100vh-6rem)]")(
            CardBody(
                hx_ext="ws",
                ws_connect="/ws",
                cls="flex-1 flex flex-col overflow-hidden"  
            )(
                Div(
                    id="chat-messages",
                    cls="flex-1 flex flex-col space-y-2 overflow-y-auto px-2",
                ),
                Form(
                    cls="flex gap-2 mt-4",
                    id="chat-form",
                    ws_send=True,
                )(
                    ChatInput(),
                )
            )
        )
    )

def component_to_html(component):
    execute = f"""
    from fasthtml.common import *
    from monsterui.all import *
    print(to_xml({component}))
    """

    result = subprocess.run(["python","-c", execute],capture_output=True,text=True)
    return result.stdout.strip()

def format_ai_message(content: Result, idx:str):
    labels = []
    # if content.doc_ids:
    #     labels = [Label(source, cls="text-primary bg-primary/10 rounded-full") for source in content.doc_ids]
    components = [render_md(content.explanation)]
    # components.append(Div(NotStr(content.component))) if content.component else None
    components.append(Div(NotStr(component_to_html(content.component)))) if content.component else None
    components.append(render_md(f"```python\n{html2ft(content.component)}\n```")) if content.component else None    
    # components.extend(labels) if labels else None
    return Div(
        Div(
            *components,  # Safely unpack the components list
            cls="p-4 bg-primary/10 rounded-lg"
        ),
        cls="max-w-[80%] mb-4",
        id="chat-messages",
        hx_swap_oob="beforeend"
    )

def ai_chunk(content: str,idx:str):
    return Span(render_md(content),id=f"chat-content-{idx}", cls="p-4 bg-primary/10 rounded-lg")

def format_user_message(content: str,idx:str):
    return Div(
        cls="flex justify-end w-full mb-4",
        id="chat-messages",
        hx_swap_oob="beforeend"
    )(
        P(
            content,
            id=idx,
            cls="p-4 bg-secondary/30 rounded-lg text-lg max-w-[80%]"
        )
    )

async def on_connect(send):
    print("Client connected")
    # result = Result(answer="Hello! I'm Void, ready to help you build web applications.", component_code="")
    # await send(format_ai_message(result, idx="welcome-chunk"))

async def on_disconnect():
    print("Client disconnected")


@rt.get("/new-chat")
async def new_chat(request):
    chat = Chat()
    chat.title = "New Chat"
    chat.user_id = UUID(json.loads(request.user).get("id"))
    chat.save()
    return RedirectResponse(f"/chat/{chat.id}", status_code=303)

@rt("/chat/{chat_id}")
@app_template("Chat", requieres="authenticated")
def page(request):
    chat_id = request.path_params.get("chat_id")
    chat = Chat.get(id=UUID(chat_id))
    return chat_section(request, chat)

@rt.ws("/ws", conn=on_connect, disconn=on_disconnect)
async def websocket_endpoint(msg: str, send):
    try:        
        # Send back user message first
        await send(format_user_message(msg, idx="user-message"))
        await send(ChatInput())
        ai_message_id = f"chat-content-{uuid.uuid4()}"

        # await send(format_ai_message("", idx=ai_message_id))
        # Get and send AI response
        # async with agent.run_stream(msg) as result:
        #     async for message in result.stream_text():  
        #         print(f"Streaming chunk to {ai_message_id}: {message[:50]}...")
        #         await send(ai_chunk(message, idx=ai_message_id))
        result = await agent.run(msg)
        print(f"Agent Result: {result.data} \n Type: {type(result.data)}")
        await send(format_ai_message(result.data,idx=ai_message_id))
        
    except Exception as e:
        print(f"Error: {str(e)}")
        await send(format_ai_message(f"I apologize, but I encountered an error: {str(e)}", idx=str(uuid.uuid4())))
