from fasthtml.components import Uk_theme_switcher
from fasthtml.common import *
from monsterui.franken import *


def theme_switcher():
    return Div(
    Button(
        UkIcon(icon='palette', uk_cloak=''),
        cls='uk-icon-button uk-icon-button-small uk-icon-button-outline'
    ),
    Div(
        Div('Customize', cls='uk-card-title uk-margin-medium-bottom'),
        Uk_theme_switcher(custom_palette="""[
            {"background": "#10b981", "key": "uk-theme-grass", "text": "Grass"},
            {"background": "#0099AD", "key": "uk-theme-lightsky", "text": "Light Sky"},
            {"background": "#E74D3C", "key": "uk-theme-mandarino", "text": "Mandarino"},
            {"background": "#364049", "key": "uk-theme-calm", "text": "Calm"}
            ]"""
        ),
        uk_drop="mode: click; offset: 8",
        cls="uk-card uk-card-body uk-card-default uk-drop uk-width-large",
    ),
    cls='uk-inline'
)

def dark_mode_style_toggle():
    """
    This is a helper function when 'dark:' tailwind modifier is not working correctly.
    """
    return Style("""
            .theme-image-light { display: flex; }
            .theme-image-dark { display: none; }
            :root[class~="dark"] .theme-image-light { display: none; }
            :root[class~="dark"] .theme-image-dark { display: flex; }
            """)
