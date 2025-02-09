from fasthtml.common import *
from monsterui.all import *
from monsterui.all import Grid as MonsterGrid
frankenui_headers = Theme.rose.headers()

app, rt = fast_app(
    pico=False,
    live=True,
    hdrs=(
        frankenui_headers,
    Script(src='https://cdn.jsdelivr.net/npm/monaco-editor@0.34.1/min/vs/loader.js'),
    Script(""" // 1) Configure Monaco so it knows where to load resources from:
    require.config({
      paths: {
        vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.34.1/min/vs'
      }
    });     
    """)
    )
)

@rt("/")
def get():
    return Titled("FastHTML Live Editor",
        H1('Monaco Editor (CDN) + HTMX Example'),
        Div(id='editor', cls='h-screen'),
        Form(
            Input(type='hidden', name='code', id='code'),
            Button('Save Editor Content', 
                type='submit',
                hx_trigger="submit",
                hx_target="#saveStatus"
            ),
            id='saveForm'
        ),
        Div(id='saveStatus'),
    )

@rt("/render")
async def post(req):
    code = (await req.json())['code']
    try:
        local_dict = {}
        exec(code, {"__builtins__": __builtins__}, local_dict)
        
        for item in local_dict.values():
            if callable(item):
                result = item()
                if isinstance(result, (FT, str)):
                    return Div(result, id="preview", hx_swap_oob="true")
        return Div("No valid component found", id="preview", hx_swap_oob="true")
    except Exception as e:
        return Div(f"Error: {str(e)}", id="preview", hx_swap_oob="true", cls="text-red-500")

serve(port=5002,reload=True)