# app/pages/index.py
from fasthtml.common import *
from fasthtml.core import APIRouter
from monsterui import *
from modules.shared.templates import page_template
from config import Settings
from .chat import chat_section
config = Settings()
rt = APIRouter()



@rt("/")
@page_template(title=config.app_name + " - Chat with Void")
def get(request):
    return chat_section()