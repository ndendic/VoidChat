# app/pages/index.py
from fasthtml.common import *
from fasthtml.core import APIRouter
from monsterui.all import *
from modules.shared.templates import page_template
from config import Settings

config = Settings()
rt = APIRouter()
hero_section = Section(
    Div(
        Img(src='https://picsum.photos/1920/1080', alt='Background Image', 
            cls='w-full h-full object-cover brightness-50'),
        Div(cls='absolute inset-0 bg-black bg-opacity-40'),
        cls='absolute inset-0'
    ),
    Div(
        H1('Welcome to Our Nonsense Hero Section', 
            cls=TextT.lead+'text-5xl md:text-6xl font-bold mb-4 text-white drop-shadow-lg'),
        P("I doesn't make sense for this site, but I'm adding it anyway", 
            cls='text-lg md:text-xl mb-8 text-gray-100 drop-shadow-md'),
        Button('Start making sense', 
            onclick="window.location.href='/auth/register'",
            cls=ButtonT.primary+'rounded-full'),
        cls='relative z-10 text-center pt-16'
    ),
    cls='relative w-full h-[50vh] bg-gray-800 flex items-start justify-center'
)

@rt("/")
@page_template("Home")
def get(request):
    return Body(
        hero_section,
    )
