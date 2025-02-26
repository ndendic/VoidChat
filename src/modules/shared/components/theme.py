from fasthtml.components import Uk_theme_switcher
from fasthtml.common import *
from monsterui.all import *


def theme_switcher():
    return Div(
    Button(
        UkIcon(icon='palette', uk_cloak=''),
        cls='uk-icon-button uk-icon-button-small uk-icon-button-outline'
    ),
    Div(
        Div('Customize', cls='uk-card-title uk-margin-medium-bottom'),
        ThemePicker(custom_themes=[
            ("Grass", "#10b981"),
            ("Light Sky", "#0099AD"),
            ("Mandarino", "#E74D3C"),
            ("Calm", "#364049")
        ]),
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
