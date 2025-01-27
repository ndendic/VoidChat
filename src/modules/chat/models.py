from datetime import datetime, timezone
from typing import ClassVar, List, Optional
from uuid import UUID
import json
import sqlalchemy
from sqlmodel import Field, Relationship
from modules.shared.models import BaseTable
from pydantic_ai.exceptions import UnexpectedModelBehavior
from pydantic_ai.messages import (
    ModelMessage,
    ModelMessagesTypeAdapter,
    ModelRequest,
    ModelResponse,
    TextPart,
    UserPromptPart,
)

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
    component_html: Optional[str] = Field(sa_type=sqlalchemy.Text, default=None)
    component_ft: Optional[str] = Field(sa_type=sqlalchemy.Text, default=None)
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
    
    def get_messages(self) -> list[ModelMessage]:
        rows = ChatMessage.filter(chat_id=self.id, sorting_field="created_at", sort_direction="asc")
        messages = []
        
        for row in rows:
            # Create a message structure that matches the expected format
            if row.role == "user":
                message_dict = {
                    "parts": [{
                        "part_kind": "user-prompt",
                        "content": row.content,
                        "timestamp": row.created_at.isoformat()
                    }],
                    "kind": "request"
                }
            else:  # assistant/model messages
                message_dict = {
                    "parts": [{
                        "part_kind": "text",
                        "content": f"{row.content} {row.component_html}",
                    }],
                    "kind": "response",
                    "timestamp": row.created_at.isoformat()
                }
            
            # Convert to JSON and validate using the adapter
            messages.extend(ModelMessagesTypeAdapter.validate_json(json.dumps([message_dict])))
        
        return messages


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
    
    # Relationships
    chat_id: UUID = Field(foreign_key="chat.id")
    chat: Chat = Relationship(back_populates="messages")
    component_html: Optional[str] = Field(sa_type=sqlalchemy.Text, default=None)

    # Admin UI metadata
    display_name: ClassVar[str] = "Chat Message"
    sidebar_icon: ClassVar[str] = "message"
    table_view_fields: ClassVar[List[str]] = ["content", "role", "chat"]
    detail_page_fields: ClassVar[List[str]] = ["content", "role", "chat"]
    field_groups: ClassVar[dict[str, List[str]]] = {
        "Message Info": ["content", "role", "chat"],
        "Timestamps": ["created_at", "updated_at"]
    }

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
    
def convert_messages_to_chat_records(json_str: str, chat_id: UUID) -> List[ChatMessage]:
    data = json.loads(json_str)
    messages = []
    
    for item in data:
        if item["kind"] == "response":
            for part in item["parts"]:
                if part["part_kind"] == "tool-call":
                    # Parse the nested args_json string
                    args = json.loads(part["args"]["args_json"])
                    
                    messages.append(ChatMessage(
                        chat_id=chat_id,
                        content=args["explanation"],  # Extract explanation as content
                        component_html=args["component"],  # Extract component as component_html
                        role="model"
                    ))
        
        elif item["kind"] == "request":
            for part in item["parts"]:
                if part["part_kind"] == "user-prompt":
                    # Process user prompt messages
                    messages.append(ChatMessage(
                        chat_id=chat_id,
                        content=part["content"],
                        component_html=None,
                        role="user"
                    ))
    
    return messages

def save_chat_messages(json_str: str, chat_id: UUID) -> List[ChatMessage]:
    messages = convert_messages_to_chat_records(json_str, chat_id)
    for message in messages:
        message.chat_id = chat_id
        message.save()
    return messages