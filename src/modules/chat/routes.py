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

def aim(text: str, code: str, idx: str):
    components = [render_md(text)]
    if code:
        preview_label = A(
            "preview",
            href="#",
            cls="ml-2 text-sm text-blue-600 underline cursor-pointer",
            hx_get=f"/chat/preview/{idx}",
            hx_target="#preview-container",
            hx_swap="outerHTML"
        )
        components.append(preview_label)
    return Div(*components, cls="p-4 bg-primary/10 rounded-lg")

def ai_message(text: str, code: str, idx: str):
    return Div(aim(text, code, idx), cls="max-w-[80%] mb-4", id="chat-messages", hx_swap_oob="beforeend")
    # return Div(render_md(text),cls="max-w-[80%] mb-4",id="chat-messages",hx_swap_oob="beforeend")

def um(content: str,idx:str):
    return DivRAligned(P(
            content,
            id=idx,
            cls="p-4 bg-secondary/30 rounded-lg text-lg max-w-[80%]"
        ))

def user_message(content: str, idx: str):
    return Div(cls="flex justify-end w-full mb-4", id="chat-messages", hx_swap_oob="beforeend")(
        um(content, idx),
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
        return CardContainer(
            id="preview-container",
            name="preview-container",
            cls="col-span-3 flex-1 flex flex-col m-4 max-h-[calc(100vh-6rem)]"
        )(
            DivFullySpaced(
                TabContainer(
                    Li(A('Preview', href='#'), cls='uk-active'),
                    Li(A('FastTags', href='#')),
                    Li(A('HTML', href='#')),
                    uk_switcher='connect: #preview; animation: uk-animation-fade',
                    alt=False,
                    cls="w-full px-2"
                )
            ),
            Ul(
                id="preview",
                cls="uk-switcher p-4"
            )(
                Li(Div(NotStr(chat.component_html))),
                Li(render_md(f"```python\n{html2ft(chat.component_html)}\n```")),
                Li(render_md(f"```html\n{chat.component_html}\n```"))
            )
        )
    else:
        return None
    
def chatbox(messages, chat):
    return CardContainer(cls="col-span-2 flex-1 flex flex-col m-4 max-h-[calc(100vh-6rem)]")(
        Script("""
            document.body.addEventListener('htmx:wsAfterMessage', function(evt) {
                const messagesDiv = document.getElementById('chat-messages');
                if (messagesDiv) {
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }
            });
        """),
        TabContainer(
            Span(
                chat.title,
                id="chat-title",
                cls=TextT.primary + " px-4 py-1 hover:underline decoration-dashed decoration-2 underline-offset-4 hover:focus-within:no-underline focus-within:bg-primary/10",
                contenteditable="plaintext-only",
                hx_post=f"/chat/{chat.id}/update-title",
                hx_trigger="blur",
                hx_swap="none",
                _onkeydown="if(event.key === 'Enter') {event.preventDefault();this.blur()}",
                _onfocus="this.value=this.textContent",
                _onblur="this.textContent = this.textContent.trim()",
                hx_vals="js:{title: document.getElementById('chat-title').textContent.trim()}"
            )
        ),
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
    return RedirectResponse(f"/chat/{chat.id}")

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
        await send(ai_message(result.data.explanation, result.data.component, idx=str(uuid.uuid4())))
        save_chat_messages(result.new_messages_json(), chat.id)
        print(f"Agent Result: {result.data} \n Type: {type(result.data)}")
        
        # Update the preview if we have a component
        if result.data.component:
            chat.component_html = result.data.component
            chat.save()
            # Send an out-of-band update for the preview container
            await send(preview_component(chat))
        
    except Exception as e:
        print(f"Error: {str(e)}")
        await send(ai_message(
            f"I apologize, but I encountered an error: {str(e)}",
            None,
            idx=str(uuid.uuid4())
        ))

@rt("/chat/{chat_id}/update-title")
async def update_title(request):
    # Get the data from the request body
    form_data = await request.form()
    title = form_data.get('title')
    print(f"Received title update request with title: {title}")
    
    chat_id = request.path_params.get("chat_id")
    chat = Chat.get(id=UUID(chat_id))
    print(f"Found chat: {chat}")
    
    if title and title.strip():  # Only update if title is not empty
        chat.title = title.strip()
        chat.save()
        print(f"Updated chat title to: {chat.title}")
    else:
        print("Title was empty or invalid")
    
    return ""  # Empty response since we're using hx-swap="none"

@rt.get("/chat/preview/{msg_id}")
def preview_message(request):
    """
    Return a preview pane for the AI message identified by msg_id,
    displaying its component code.
    """
    msg_id = request.path_params.get("msg_id")
    # Retrieve the AI message by its ID.
    ai_msg = ChatMessage.get(id=UUID(msg_id))
    if ai_msg and ai_msg.component_html:
         return CardContainer(
             id="preview-container",
             name="preview-container",
             cls="col-span-3 flex-1 flex flex-col m-4 max-h-[calc(100vh-6rem)]"
         )(
             DivFullySpaced(
                 TabContainer(
                     Li(A('Preview', href='#'), cls='uk-active'),
                     Li(A('FastTags', href='#')),
                     Li(A('HTML', href='#')),
                     uk_switcher='connect: #preview; animation: uk-animation-fade',
                     alt=False,
                     cls="w-full px-2"
                 )
             ),
             Ul(
                 id="preview",
                 cls="uk-switcher p-4"
             )(
                 Li(Div(NotStr(ai_msg.component_html))),
                 Li(render_md(f"```python\n{html2ft(ai_msg.component_html)}\n```")),
                 Li(render_md(f"```html\n{ai_msg.component_html}\n```"))
             )
         )
    return ""