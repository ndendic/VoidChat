# app/pages/index.py
from fasthtml.common import *
from fasthtml.core import APIRouter
from monsterui import *
from modules.shared.templates import page_template
from config import Settings
from .chat import chat_section
from modules.public.components.navbar import Navbar

config = Settings()
rt = APIRouter()



@rt("/")
def get(request):
    return Title(config.app_name + " - Chat with Void"), Body(
        Navbar(),
        chat_section()
    )