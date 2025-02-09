import subprocess
import json
from typing import List
from uuid import UUID, uuid4
from fasthtml.common import *
from modules.chat.models import Chat, ChatMessage
from modules.chat.agent import agent
from pydantic_ai import Agent

simple_agent = Agent(
    'openai:gpt-4o-mini',
    retries=3,
    system_prompt="You are a helpful assistant"
)
# for cm in ChatMessage.filter(chat_id=UUID("d3baad28-ad0a-43fe-80a0-500e84f0ef25")):
#     if cm.role == "assistant":
#         cm.role = "model"
#         cm.save()
#         print(f"Updated {cm.id} to {cm.role}")

# chat = Chat.get(id = UUID("d3baad28-ad0a-43fe-80a0-500e84f0ef25"))
# messages = chat.get_messages()
# print(messages)
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

# chat = Chat(title="Test Chat", user_id=UUID("8cc3f47964d842a8895e99e007637989"))
# chat.save()
# print(chat.id)
response = simple_agent.run_sync("Hello there!")
nm = response.new_messages()
print(nm)
nmj = response.new_messages_json()
print(nmj)

# messages = convert_messages_to_chat_records(response.new_messages_json(), chat.id)
# for message in messages:
#     print(message)    
#     message.save()

# print(chat.get_messages())

# component = """
# Div(
#     H1("Subtest")
# )
# """
# execute = f"""
# from fasthtml.common import *
# from monsterui.all import *
# print(to_xml({component}))
# """

# result = subprocess.run(["python","-c", execute],capture_output=True,text=True)
# print(result)
# print(result.stdout.strip())

# read md file content
# style_guide = ""
# with open(".llms/styling-guide.md", "r") as file:
#     style_guide = file.read()
# print(style_guide)
