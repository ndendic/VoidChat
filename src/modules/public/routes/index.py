# app/pages/index.py
from fasthtml.common import *
from fasthtml.core import APIRouter
from monsterui import *
from monsterui.all import *
from modules.shared.templates import page_template
from config import Settings

config = Settings()
rt = APIRouter()

def chat_section():
    return Main(
        cls="flex flex-col items-center justify-center h-screen px-4 bg-background"
    )(
        Card(
            cls="w-full max-w-4xl mx-auto bg-card"
        )(
            CardBody(
                # Chat messages container
                Div(
                    id="chat-messages",
                    cls="flex flex-col space-y-2 overflow-y-auto min-h-[500px] max-h-[700px] mb-4",
                    hx_ext="ws",  # Enable WebSocket extension
                    ws_connect="/ws"  # WebSocket connection endpoint
                ),
                # Chat input form with WebSocket
                Form(
                    cls="flex gap-2",
                    id="chat-form",
                    ws_send=True,  # Enable WebSocket sending
                )(
                    Input(
                        id="msg",
                        name="msg",
                        placeholder="Type your message...",
                        cls="flex-1",
                        required=True,
                        autofocus=True
                    ),

                )
            )
        )
    )

def features_section():
    return Section(
        cls="py-16 bg-muted/50"
    )(
        Container(
            H2("What I can help you with", cls="text-2xl font-bold text-center mb-8"),
            Grid(
                Card(
                    CardBody(
                        H3("MonsterUI Components", cls="text-lg font-semibold mb-2"),
                        P("Build beautiful, responsive UI components using MonsterUI's modern design system")
                    ),
                    cls="p-6"
                ),
                Card(
                    CardBody(
                        H3("FastHTML Integration", cls="text-lg font-semibold mb-2"),
                        P("Create dynamic web applications with FastHTML's powerful routing and templating")
                    ),
                    cls="p-6"
                ),
                Card(
                    CardBody(
                        H3("Real-time Updates", cls="text-lg font-semibold mb-2"),
                        P("Implement HTMX-powered real-time features without complex JavaScript")
                    ),
                    cls="p-6"
                ),
                cls="grid-cols-1 md:grid-cols-3 gap-6"
            )
        )
    )

@rt("/")
@page_template(title=config.app_name + " - Chat with Void")
def get(request):
    return chat_section()