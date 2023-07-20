from flask import jsonify
from typing import Dict, Tuple
from db.models import UserToChats
from logger import with_logging
from statistics import Statistics
from app import logger

REQUEST_ERROR = "Request error: "


@with_logging
@staticmethod
def statistics_handler(user_to_chat_id: int) -> Tuple[Dict, int]:
    if request_is_valid(user_to_chat_id):
        return get_statistics(user_to_chat_id)


@with_logging
def request_is_valid(user_to_chat_id: int) -> bool:
    record = UserToChats.query.get(user_to_chat_id)
    if record is None:
        raise Exception(f"{REQUEST_ERROR}Invalid user_to_chat_id")
    return True


@with_logging
def get_statistics(user_to_chat_id: int) -> Tuple[Dict, int]:
    statistics = Statistics(user_to_chat_id)
    as_json = jsonify(statistics.to_json())
    logger.info(f"Nadav {statistics.to_json()}")
    return as_json, 200
