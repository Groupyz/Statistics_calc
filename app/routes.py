from app import app
from flask import request
from api.api_file_handler import handle_file, REQUEST_ERROR
from api.api_statistics_handler import statistics_handler
from logger import with_logging
from typing import Dict, Tuple


@app.route("/")
def hello():
    return "Hello World :)"


@with_logging
@app.route("/createChat", methods=["POST"])
async def create_chat():
    try:
        return await handle_file(request)
    except Exception as e:
        if str(e).startswith(REQUEST_ERROR):
            return str(e), 400
        else:
            return str(e), 500


@with_logging
@app.route("/statistics/<int:user_to_chat_id>", methods=["GET"])
def get_statistics(user_to_chat_id) -> Tuple[Dict, int]:
    try:
        return statistics_handler(user_to_chat_id)
    except Exception as e:
        if str(e).startswith(REQUEST_ERROR):
            return str(e), 400
        else:
            return str(e), 500
