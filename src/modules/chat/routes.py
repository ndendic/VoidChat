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
from .coder_agent import agent as coder_agent, CodeResult
from .chat_agent import propose_title
from uuid import UUID
from modules.admin.components.sidebar import SidebarButton

config = Settings()
rt = APIRouter()
messages = []

def ai_chunk(content: str,idx:str):
    return Span(render_md(content),id=f"chat-content-{idx}", cls="p-4 bg-primary/10 rounded-lg")

def aim(text: str, code: str, idx: str, html_output: str = None):
    components = [render_md(text, class_map_mods={'p': 'mb-1'})]
    if code:
        preview_label = Label(
            "preview",
            cls="cursor-pointer bg-primary/50",
            hx_get=f"/chat/preview/{idx}",
            hx_target="#preview-container",
            hx_swap="outerHTML"
        )
        components.append(preview_label)
    return Div(*components, cls="p-4 bg-primary/10 rounded-lg")


def ai_message(text: str, code: str, idx: str, html_output: str = None):
    return Div(aim(text, code, idx, html_output), cls="max-w-[80%] mb-4", id="chat-messages", hx_swap_oob="beforeend")
    # return Div(render_md(text),cls="max-w-[80%] mb-4",id="chat-messages",hx_swap_oob="beforeend")

def um(content: str,idx:str):
    return DivRAligned(P(
            content,
            id=idx,
            cls="p-4 bg-secondary/30 rounded-lg max-w-[80%]"
        ))

def user_message(content: str, idx: str):
    return Div(cls="flex justify-end w-full mb-4", id="chat-messages", hx_swap_oob="beforeend")(
        um(content, idx),
    )
    
def ChatInput():
    return Input(
            id="msg",
            name="msg",
            placeholder="Type your message...",
            cls="flex-1",
            required=True,
            autofocus=True,
        )

def preview_component(chat):
    html = chat.component_html if chat.component_html else "<p>Your AI has not generated any components yet.</p>"
    ft_code = chat.component_ft if chat.component_ft else "<p>Your AI has not generated any components yet.</p>"
    return CardContainer(
        id="preview-container",
        name="preview-container",
        cls="col-span-3 flex flex-col m-4 max-h-[calc(100vh-6rem)] overflow-auto"
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
                Li(Div(NotStr(html))),
                Li(render_md(f"```python\n{ft_code}\n```")),
                Li(render_md(f"```html\n{html}\n```"))
            )
        )
   
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
            DivFullySpaced(
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
                ),
                UkIconLink(
                    href=f"/chat/{chat.id}/delete",
                    icon="trash",
                    cls="text-red-500 hover:text-red-600"
                )
            ),
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


@rt("/new-chat")
async def new_chat(request):
    form_data = await request.form()
    initial_message = form_data.get("msg", "")
    print(f"Initial Message: {initial_message}")
    print(f"Form Data: {form_data}")
    chat = Chat()
    chat.title = await propose_title(initial_message)
    chat.user_id = UUID(json.loads(request.user).get("id"))
    chat.save()
    if initial_message:
        result = await coder_agent.run(initial_message)
        save_chat_messages(result.new_messages_json(), chat.id)
        if result.data.python_code or result.data.html_output:
            chat.component_ft = result.data.python_code if result.data.python_code else ""
            chat.component_html = result.data.html_output if result.data.html_output else ""
            chat.save()

    new_sidebar_item = SidebarButton("message-circle-code", chat.title, f"/chat/{chat.id}")
    from fasthtml.common import to_xml
    new_sidebar_html = to_xml(new_sidebar_item)
    response = HTMLResponse(new_sidebar_html)
    response.headers["HX-Redirect"] = f"/chat/{chat.id}"
    return response

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
        history = chat.get_messages()

        result = await coder_agent.run(msg, message_history=history)
        await send(ai_message(result.data.explanation, result.data.python_code, idx=str(uuid.uuid4()), html_output=result.data.html_output))
        save_chat_messages(result.new_messages_json(), chat.id)
        # Update the preview if we have a component
        if result.data.python_code or result.data.html_output:
            chat.component_ft = result.data.python_code if result.data.python_code else ""
            chat.component_html = result.data.html_output if result.data.html_output else ""
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
    chat_id = request.path_params.get("chat_id")
    chat = Chat.get(id=UUID(chat_id))
    
    if title and title.strip():
        chat.title = title.strip()
        chat.save()
    
    # Return an out-of-band swap that updates the sidebar chat title
    return P(
        chat.title,
        id=f"sidebar-chat-{chat.id}",
        cls="sidebar-text text-muted-foreground",
        hx_swap_oob="outerHTML"
    )

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

@rt.get("/chat/{chat_id}/delete")
async def delete_chat(request):
    chat_id = request.path_params.get("chat_id")
    Chat.delete_record(id=UUID(chat_id))
    return RedirectResponse(url="/dashboard")