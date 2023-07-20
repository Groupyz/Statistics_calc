from dataclasses import dataclass
from db.models import UserToChats, Message
from logger import with_logging
from app import db, logger
from sqlalchemy import func
import json


@dataclass
class ChatMacroDetails:
    name: str
    id: int
    num_of_messages: int

    @with_logging
    def __init__(self, chat_id: int) -> None:
        chat = UserToChats.query.filter_by(id=chat_id).first()
        self.name = chat.chat_name
        self.id = chat.id
        self.num_of_messages = Message.query.filter_by(chat_id=chat_id).count()


@dataclass
class ChatMicroDetails:
    name_to_num_of_messages: dict

    @with_logging
    def __init__(self, chat_id: int) -> None:
        query = (
            db.session.query(
                Message.contact_name, func.count(Message.id).label("amount_of_messages")
            )
            .filter(Message.chat_id == chat_id)
            .group_by(Message.contact_name)
            .order_by(Message.contact_name)
        )
        list_with_tuples = query.all()
        self.name_to_num_of_messages = {item[0]: item[1] for item in list_with_tuples}
        logger.info(self.name_to_num_of_messages)


class Statistics:
    macro_details: ChatMacroDetails
    micro_details: ChatMicroDetails

    def __init__(self, chat_id: int) -> None:
        self.macro_details = ChatMacroDetails(chat_id)
        self.micro_details = ChatMicroDetails(chat_id)

    def to_json(self) -> str:
        data = {
            "macro_details": {
                "name": self.macro_details.name,
                "id": self.macro_details.id,
                "num_of_messages": self.macro_details.num_of_messages,
            },
            "micro_details": {
                "name_to_num_of_messages": self.micro_details.name_to_num_of_messages
            },
        }
        return json.dumps(data)
