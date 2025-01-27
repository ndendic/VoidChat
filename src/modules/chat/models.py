from datetime import datetime, timezone
from typing import ClassVar, List, Optional
from uuid import UUID
import sqlalchemy
from sqlmodel import Field, Relationship
from modules.shared.models import BaseTable

class Chat(BaseTable, table=True):
    """
    Chat model for storing chat sessions.
    """
    title: str = Field(
        index=True,
        title="Chat Title",
        schema_extra={"icon": "chat", "input_type": "text"}
    )
    user_id: UUID = Field(foreign_key="user.id")

    # Relationships
    messages: List["ChatMessage"] = Relationship(back_populates="chat")

    # Admin UI metadata
    display_name: ClassVar[str] = "Chat"
    sidebar_icon: ClassVar[str] = "chat"
    table_view_fields: ClassVar[List[str]] = ["title", "messages", "created_at"]
    detail_page_fields: ClassVar[List[str]] = ["title", "messages", "created_at"]
    field_groups: ClassVar[dict[str, List[str]]] = {
        "Basic Info": ["title", "messages"],
        "Timestamps": ["created_at", "updated_at"]
    }

    def __str__(self):
        return self.title


class ChatMessage(BaseTable, table=True):
    """
    ChatMessage model for storing individual messages within a chat.
    """
    content: str = Field(
        sa_type=sqlalchemy.Text,
        title="Message Content",
        schema_extra={"icon": "message", "input_type": "textarea"}
    )
    role: str = Field(
        title="Message Role",
        schema_extra={"icon": "user", "input_type": "select", "choices": ["user", "model"]}
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        title="Message Timestamp",
        schema_extra={"icon": "clock"}
    )
    
    # Relationships
    chat_id: UUID = Field(foreign_key="chat.id")
    chat: Chat = Relationship(back_populates="messages")

    # Admin UI metadata
    display_name: ClassVar[str] = "Chat Message"
    sidebar_icon: ClassVar[str] = "message"
    table_view_fields: ClassVar[List[str]] = ["content", "role", "chat", "timestamp"]
    detail_page_fields: ClassVar[List[str]] = ["content", "role", "chat", "timestamp"]
    field_groups: ClassVar[dict[str, List[str]]] = {
        "Message Info": ["content", "role", "chat"],
        "Timestamps": ["timestamp", "created_at", "updated_at"]
    }

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."