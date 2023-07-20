from transformers.json_to_data import *
from transformers.txt_to_json import TxtToJsonConverter
from flask import request
from typing import Tuple, Any
from logger import with_logging
from app import logger
import asyncio


REQUEST_ERROR = "Request error: "
SERVER_ERROR = "Server error: "
SERVER_ERROR_WHILE_CREATING_RECORDS = (
    SERVER_ERROR + "Error while creating records in db: "
)


@staticmethod
async def handle_file(request: request) -> Tuple[str, int]:
    if request_is_valid(request):
        await turn_file_into_record(request)
        return "File uploaded successfully", 201


@staticmethod
def request_is_valid(request: request) -> bool:
    if "file" not in request.files:
        raise Exception(REQUEST_ERROR + "No file found")
    elif "user_id" not in request.form:
        raise Exception(REQUEST_ERROR + "No user Id found")
    file = request.files["file"]
    if file.filename == "":
        raise Exception(REQUEST_ERROR + "Empty file name")
    elif not file.filename.endswith(".txt"):
        raise Exception(
            REQUEST_ERROR + "Invalid file type. Only .txt files are allowed"
        )

    return True


@staticmethod
async def turn_file_into_record(request: request):
    try:
        user_id, file = get_data_from(request)
        file.save(file.filename)
        await create_records_in_db_from(user_id, file)
    except Exception as e:
        raise Exception(SERVER_ERROR_WHILE_CREATING_RECORDS + str(e))


def get_data_from(request: request) -> Tuple[str, Any]:
    user_id = request.form["user_id"]
    file = request.files["file"]

    return user_id, file


async def process_messages(messages: list[Message], chat_id: int) -> None:
    tasks = []
    for message in messages:
        task = asyncio.create_task(create_message_rec(message, chat_id))
        tasks.append(task)

    await asyncio.gather(*tasks)


async def create_records_in_db_from(user_id: str, file):
    try:
        messages_as_json = TxtToJsonConverter(file.filename).convert_to_json()
        chat_id = create_chat_rec(user_id, file.filename)
        messages_as_ds = Json_to_Data_Converter(messages_as_json).messages
        await process_messages(messages_as_ds, chat_id)
    except Exception as e:
        logger.exception(SERVER_ERROR_WHILE_CREATING_RECORDS + str(e))
        raise Exception(SERVER_ERROR_WHILE_CREATING_RECORDS + str(e))
