from fasthtml.common import *
from fasthtml.core import APIRouter
from pydantic_ai import Agent
from config import Settings
from monsterui.all import *
import uuid

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
            hx_swap_oob='true'
        )
def chat_section():
    return Main(
        cls="flex flex-col items-center justify-center h-screen px-4 bg-background"
    )(
        Card(
            cls="w-full max-w-4xl mx-auto bg-card"
        )(
            CardBody(hx_ext="ws",  # Enable WebSocket extension
                    ws_connect="/ws"  # WebSocket connection endpoint   
                )(
                # Chat messages container
                Div(
                    id="chat-messages",
                    cls="flex flex-col space-y-2 overflow-y-auto min-h-[500px] max-h-[700px] mb-4",
                    
                ),
                # Chat input form with WebSocket
                Form(
                    cls="flex gap-2",
                    id="chat-form",
                    ws_send=True,  # Enable WebSocket sending
                )(
                    ChatInput(),

                )
            )
        )
    )

# Initialize the AI agent
agent = Agent(
    'openai:gpt-4o-mini',
    system_prompt='You are Void, an AI assistant specialized in helping developers build web applications using MonsterUI and FastHTML. Be concise and helpful.'
)

def format_ai_message(content: str, idx:str):
    return Div(
        Div(render_md(content), id=f"chat-content-{idx}", cls="p-4 bg-primary/10 rounded-lg"),
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
    await send(format_ai_message("Hello! I'm Void, ready to help you build web applications.", idx="welcome-chunk"))

async def on_disconnect():
    print("Client disconnected")

@rt.ws("/ws", conn=on_connect, disconn=on_disconnect)
async def websocket_endpoint(msg: str, send):
    try:        
        # Send back user message first
        print(f"Received message: {msg}")
        await send(format_user_message(msg, idx="user-message"))
        await send(ChatInput())
        ai_message_id = f"chat-content-{uuid.uuid4()}"

        print(f"Created container with ID: {ai_message_id}")
        await send(format_ai_message("", idx=ai_message_id))
        # Get and send AI response
        async with agent.run_stream(msg) as result:
            async for message in result.stream_text():  
                print(f"Streaming chunk to {ai_message_id}: {message[:50]}...")
                await send(ai_chunk(message, idx=ai_message_id))
        # result = await agent.run(msg)
        # print(result.data)
        # await send(format_ai_message(result.data))
        
    except Exception as e:
        print(f"Error: {str(e)}")
        await send(format_ai_message(f"I apologize, but I encountered an error: {str(e)}", idx=str(uuid.uuid4())))

def chat_page():
    return Container(
        Div(
            # This will be the messages container
            id="chat-messages",
            cls="flex flex-col space-y-2 overflow-y-auto max-h-[600px]"
        ),
        # Your input form below
        Form(
            Input(name="message", placeholder="Type your message..."),
            hx_ws="connect:/ws"  # WebSocket connection
        )
    )
