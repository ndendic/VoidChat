import json
import uuid
import subprocess
from datetime import datetime, timezone

from config import Settings

from starlette.responses import RedirectResponse
from fasthtml.common import *
from fasthtml.core import APIRouter
from monsterui.all import *
from modules.shared.templates import app_template

from .models import ChatMessage, Chat, save_chat_messages
from .agent import agent, HTMLResult
from uuid import UUID

config = Settings()
rt = APIRouter()
messages = []

def component_to_html(component):
    cmd = f"""
    from fasthtml.common import *
    from monsterui.all import *
    print(to_xml({component}))
    """

    result = subprocess.run(["python","-c", cmd],capture_output=True,text=True)
    return result.stdout.strip()

def ai_chunk(content: str,idx:str):
    return Span(render_md(content),id=f"chat-content-{idx}", cls="p-4 bg-primary/10 rounded-lg")

def aim(text: str, code: str, idx:str):
    components = [render_md(text)]
    # if code:
    #     components.append(
    #         Div(cls="bg")(
    #             DivFullySpaced(TabContainer(
    #                 Li(A('Preview',    href='#'),    cls='uk-active'),
    #                 Li(A('Code', href='#')),
    #                 uk_switcher=f'connect: #component-{idx}; animation: uk-animation-fade',
    #                 alt=True,
    #                 cls="max-w-80"
    #         )),
    #         Ul(id=f"component-{idx}", cls="uk-switcher")(
    #                 Li(Div(NotStr(code))),
    #                 Li(render_md(f"```python\n{html2ft(code)}\n```"))
    #             )
    #         )
    #     )
    return Div( *components, cls="p-4 bg-primary/10 rounded-lg")

def ai_message(text: str, code: str, idx:str):
    return Div(aim(text, code, idx),cls="max-w-[80%] mb-4",id="chat-messages",hx_swap_oob="beforeend")
    # return Div(render_md(text),cls="max-w-[80%] mb-4",id="chat-messages",hx_swap_oob="beforeend")

def um(content: str,idx:str):
    return DivRAligned(P(
            content,
            id=idx,
            cls="p-4 bg-secondary/30 rounded-lg text-lg max-w-[80%]"
        ))

def user_message(content: str,idx:str):
    return Div(cls="flex justify-end w-full mb-4",id="chat-messages",hx_swap_oob="beforeend")(
        um(content,idx), 
        Loading((LoadingT.dots, LoadingT.md), htmx_indicator=True)
    )
    
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

def preview_component(chat):
    if chat.component_html:
        return CardContainer(cls="col-span-3 flex-1 flex flex-col m-4 max-h-[calc(100vh-6rem)]")(
            DivFullySpaced(TabContainer(
                Li(A('Preview',    href='#'),    cls='uk-active'),
                Li(A('Code', href='#')),
                uk_switcher='connect: #preview; animation: uk-animation-fade',
                alt=False,
                cls="w-full px-2"
            )),
            Ul(id="preview", cls="uk-switcher p-4")(
                Li(Div(NotStr(chat.component_html))),
                Li(render_md(f"```python\n{html2ft(chat.component_html)}\n```"))
            )
        )
    else:
        return None
    
def chatbox(messages, chat):
    return CardContainer(cls="col-span-2 flex-1 flex flex-col m-4 max-h-[calc(100vh-6rem)]")(
            TabContainer(Span(chat.title,cls=TextT.primary +"px-4 py-1")),
            CardBody(
                hx_ext="ws",
                ws_connect=f"/ws/{chat.id}",
                cls="flex-1 flex flex-col overflow-hidden"  
            )(
                Div(
                    *messages,
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

def chat_section(request, chat):
    mesgs = ChatMessage.filter(chat_id=chat.id, sorting_field="created_at", sort_direction="asc")
    messages = []
    for msg in mesgs:
        if msg.role == "user":            
            messages.append(um(msg.content, msg.id))
        else:
            messages.append(aim(msg.content, msg.component_html, msg.id))
    return Grid(cols=5,cls="min-h-[calc(100vh-4rem)] flex flex-col", id="chat-container")(
        chatbox(messages, chat),
        preview_component(chat)      
    )


@rt.get("/new-chat")
async def new_chat(request):
    chat = Chat()
    chat.title = "New Chat"
    chat.user_id = UUID(json.loads(request.user).get("id"))
    chat.save()
    return RedirectResponse(f"/chat/{chat.id}", status_code=303)

async def on_connect(websocket):
    print("Client connected")

async def on_disconnect(websocket):
    print("Client disconnected")

@rt("/chat/{chat_id}")
@app_template("Chat", requieres="authenticated")
def page(request):
    chat_id = request.path_params.get("chat_id")
    chat = Chat.get(id=UUID(chat_id))
    return chat_section(request, chat)

@rt.ws("/ws/{chat_id}", conn=on_connect, disconn=on_disconnect)
async def websocket_endpoint(msg: str, websocket: WebSocket, send):
    try:
        chat = Chat.get(id=UUID(websocket.path_params['chat_id']))                    
        # Send back user message first
        await send(user_message(msg, idx="user-message"))
        await send(ChatInput())
        # Get and send AI response
        history = chat.get_messages()
        result = await agent.run(msg, message_history=history)
        await send(ai_message(result.data.explanation,result.data.component,idx=str(uuid.uuid4())))
        save_chat_messages(result.new_messages_json(), chat.id)
        print(f"Agent Result: {result.data} \n Type: {type(result.data)}")
        if result.data.component:
            chat.component_html = result.data.component
            chat.save()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        # Make sure to include all required fields for HTMLResult
        await send(ai_message(
            f"I apologize, but I encountered an error: {str(e)}",
            None,
            idx=str(uuid.uuid4())
        ))
