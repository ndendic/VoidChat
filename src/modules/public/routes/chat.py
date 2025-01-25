from fasthtml.common import *
from fasthtml.core import APIRouter
from monsterui import *
from pydantic_ai import Agent
from config import Settings

config = Settings()
rt = APIRouter()

# Initialize the AI agent
agent = Agent(
    'openai:gpt-4o-mini',
    system_prompt='You are Void, an AI assistant specialized in helping developers build web applications using MonsterUI and FastHTML. Be concise and helpful.'
)

def format_ai_message(content: str):
    return Div(
        P(content, cls="p-4 bg-primary/10 rounded-lg"),
        cls="chat-message ai-message max-w-[80%] mb-4",
        id="chat-messages",
        hx_swap_oob="beforeend"
    )

def format_user_message(content: str):
    return Div(
        cls="flex justify-end w-full mb-4",
        id="chat-messages",
        hx_swap_oob="beforeend"
    )(
        P(
            content,
            cls="p-4 bg-secondary/10 rounded-lg text-lg max-w-[80%]"
        )
    )

async def on_connect(send):
    print("Client connected")
    await send(format_ai_message("Hello! I'm Void, ready to help you build web applications."))

async def on_disconnect():
    print("Client disconnected")

@rt.ws("/ws", conn=on_connect, disconn=on_disconnect)
async def websocket_endpoint(msg: str, send):
    try:
        # Send back user message first
        await send(format_user_message(msg))
        
        # Get and send AI response
        result = await agent.run(msg)
        print(result.data)
        await send(format_ai_message(result.data))
        
    except Exception as e:
        print(f"Error: {str(e)}")
        await send(format_ai_message(f"I apologize, but I encountered an error: {str(e)}"))

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
