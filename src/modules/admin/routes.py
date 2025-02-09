from typing import Type

from fasthtml.common import *
from fasthtml.core import APIRouter
from fasthtml.svg import *
from monsterui import *
from monsterui.all import *
from monsterui.franken import Grid as Grd

from modules.shared.models import BaseTable
from modules.shared.templates import app_page, app_template, is_htmx
from .components.dashboard import dashboard_page
from modules.chat.routes import ChatInput
rt = APIRouter()


@rt("/dashboard")
@app_template("Dashboard", requieres="authenticated")
def page(request):
    return Container(cls="flex items-center justify-center min-h-[80vh] w-full")(
            Form(
                cls="w-full max-w-2xl",  # Limits form width and centers it
                id="chat-form",
                hx_post="/new-chat",
            )(
                ChatInput(),
                P(Loading(htmx_indicator=True),"Working on it...",cls="mt-2 htmx-indicator")
            )
    )


def find_base_table_class(table_name: str) -> Type[BaseTable]:
    for subclass in BaseTable.__subclasses__():
        if subclass.__name__.lower() == table_name.lower():
            return subclass
    return None


@rt("/table/{table}")
def get(request, table: str = ""):
    if table:
        model: BaseTable = find_base_table_class(table)
        if model:
            if is_htmx(request):
                return model.render_table(request)
            else:
                return app_page("Table", request, model.render_table(request))
        else:
            return Div(f"Model {table} not found.")
    else:
        return H1("Table not found")


@rt("/table/{table}/search")
def get(request, table: str = ""):
    model: BaseTable = find_base_table_class(table)
    if model:
        return model.render_table(request, records_only=True)
    else:
        return H1("Table not found")


@rt("/table/{table}/{record_id}")
def get(request, table: str = "", record_id: str = ""):
    model_class = find_base_table_class(table)
    if model_class:
        if record_id == "new":
            return model_class()
        else:
            record = model_class.get(record_id)
            if record:
                return record
            else:
                return H1("Record not found")
    else:
        return H1("Table not found")


@rt("/table/{table}/upsert")
async def post(request, table: str = ""):
    model: BaseTable = find_base_table_class(table)
    form_data = await request.form()
    processed_data = dict(form_data)

    for key, value in processed_data.items():
        if value == "on":  # If it's a checkbox value
            processed_data[key] = True
        elif value == "":  # If checkbox is unchecked, it won't be in form data
            processed_data[key] = False

    if model:
        if model.upsert(processed_data):
            return model.render_table(request, records_only=True)
    else:
        return H1("Table not found")


@rt("/table/{table}/{record_id}")
def delete(request, table: str = "", record_id: str = ""):
    model: BaseTable = find_base_table_class(table)
    if model:
        model.delete_record(record_id)
        return model.render_table(request, records_only=True)
    else:
        return H1("Table not found")
