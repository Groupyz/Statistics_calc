from app import db
from db.models import UserToChats, Message as MessageModel
from logger import with_logging
from dataclasses import dataclass, field


@dataclass
class Message:
    date: str
    time: str
    name: str
    text: str


@dataclass
class Json_to_Data_Converter:
    messages: list[Message] = field(default_factory=list)

    def __init__(self, json_array):
        self.json_array = json_array
        self.messages = self.convert_json_to_messages()

    @with_logging
    def convert_json_to_messages(self) -> list[Message]:
        messages = []
        for curMessage in self.json_array:
            datetime = curMessage.get("datetime")
            date = datetime.get("date")
            time = datetime.get("time")
            name = curMessage.get("name")
            text = curMessage.get("text")
            message = Message(date=date, time=time, name=name, text=text)
            messages.append(message)

        return messages


@with_logging
@staticmethod
def create_chat_rec(user_id: str, chat_name: str) -> int:
    new_chat_rec = UserToChats(chat_name=chat_name, user_id=user_id)
    db.session.add(new_chat_rec)
    db.session.commit()

    return new_chat_rec.id


@staticmethod
async def create_message_rec(message: Message, user_to_chat_id: int):
    date, time, name, text = (
        message.date,
        message.time,
        message.name,
        message.text,
    )
    message = MessageModel(
        date=date, time=time, contact_name=name, text=text, chat_id=user_to_chat_id
    )
    db.session.add(message)
    db.session.commit()
