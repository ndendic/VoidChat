from fasthtml.common import *
from fasthtml.core import APIRouter
from monsterui.all import *
from modules.shared.templates import app_template

rt = APIRouter()

def publish_component_modal():
    """
    Returns a modal dialog for setting the name, description, and tags for a component.
    """
    return Modal(
        Div(cls="p-6")(
            ModalTitle("Publish Component"),
            P("Fill out the information below to publish your component."),
            Form(
                LabelInput("Component Name", id="component-name", placeholder="Enter component name"),
                LabelTextArea("Description", id="component-description", placeholder="Enter a short description"),
                LabelInput("Tags", id="component-tags", placeholder="Comma-separated tags"),
                DivRAligned(
                    ModalCloseButton("Cancel", cls=ButtonT.ghost),
                    Button(
                        "Publish",
                        cls=ButtonT.primary,
                        type="submit",
                        hx_post="/gallery/publish",
                        hx_target="#gallery-container",
                        hx_swap="outerHTML"
                    )
                ),
                cls="space-y-4"
            )
        ),
        id="publish-component-modal"
    )

@rt('/gallery')
@app_template("Component Gallery", requieres="authenticated")
def gallery_page(request):
    """
    Displays all created components along with a "Publish" button for each.
    """
    # Placeholder list of components -- replace with your own database query as needed
    components = [
        {"name": "Component 1", "description": "A sample component", "tags": "sample, demo"},
        {"name": "Component 2", "description": "Another component", "tags": "example, ui"}
    ]
    
    component_cards = []
    for comp in components:
        card = Card(
            H4(comp["name"]),
            P(comp["description"]),
            P("Tags: " + comp["tags"], cls="text-muted"),
            # The publish button fetches the modal content when clicked
            Button(
                "Publish",
                cls=ButtonT.primary,
                hx_get="/gallery/publish-modal",
                hx_target="#modal-container",
                hx_swap="innerHTML"
            )
        )
        component_cards.append(card)
    ButtonT.primary
    return Div(
        Div(
            H2("Component Gallery"),
            Div(*component_cards, id="gallery-container", cls="grid grid-cols-3 gap-4"),
            # This container will host the modal dialog when the publish button is clicked
            Div(id="modal-container")
        ),
        cls="p-8"
    )

@rt.get('/gallery/publish-modal')
def get_publish_modal(request):
    """
    Returns the modal dialog when a publish button is clicked.
    """
    return publish_component_modal()

@rt.post('/gallery/publish')
async def publish_component(request):
    """
    Handles the form submission from the publish modal.
    """
    form_data = await request.form()
    component_name = form_data.get("component-name")
    description = form_data.get("component-description")
    tags = form_data.get("component-tags")
    
    # Save the component's metadata to your database here.
    # For the purpose of this example we just return a success message.
    return Div(
        P(f"Component '{component_name}' published successfully!"),
        cls="p-4 bg-green-200 text-green-800 rounded-lg"
    )

# Add other HTTP methods as needed
