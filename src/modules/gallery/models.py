from modules.shared.models import BaseTable
from datetime import datetime
from pydantic import Field

class Component(BaseTable, table=True):
    """
    Gallery model for storing gallery related data.
    """
    name: str
    description: str
    tags: list[str]
    code: str
