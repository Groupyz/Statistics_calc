import pytest
from app import app
from transformers.json_to_data import *
from db.models import UserToChats, Message as MessageModel
from logger import with_logging
import asyncio


class TestJsonToDataConverter:
    @with_logging
    def test_convert_json_to_messages(self):
        json_array = [
            {
                "datetime": {"date": "11/21/22", "time": "22:16"},
                "name": "Omer LeiBo",
                "text": "לא הוא עוד לא ענה, שלחתי לו אתמול עוד תזכורת במייל אבל מחר אני כבר אשלח לו הודעה",
            },
            {
                "datetime": {"date": "11/21/22", "time": "22:21"},
                "name": "Ns",
                "text": "חיה, תודה👌🏿",
            },
        ]

        converter = Json_to_Data_Converter(json_array)
        messages = converter.messages

        assert len(messages) == 2

        # Check the attributes of the first message
        assert messages[0].date == "11/21/22"
        assert messages[0].time == "22:16"
        assert messages[0].name == "Omer LeiBo"
        assert (
            messages[0].text
            == "לא הוא עוד לא ענה, שלחתי לו אתמול עוד תזכורת במייל אבל מחר אני כבר אשלח לו הודעה"
        )

        # Check the attributes of the second message
        assert messages[1].date == "11/21/22"
        assert messages[1].time == "22:21"
        assert messages[1].name == "Ns"
        assert messages[1].text == "חיה, תודה👌🏿"


@pytest.fixture(scope="module")
def db_session():
    flask_app = app
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@with_logging
def test_create_chat_rec(db_session):
    # Input data for testing
    user_id = "example_user_id"
    chat_name = "example_chat_name"

    # Call the method being tested
    create_chat_rec(user_id, chat_name)

    # Retrieve the record from the database
    chat_rec = UserToChats.query.filter_by(user_id=user_id).first()

    # Assert that the record was created successfully
    assert chat_rec is not None
    assert chat_rec.user_id == user_id
    assert chat_rec.chat_name == chat_name


@pytest.fixture
def mock_message():
    return Message("2023-07-05", "10:30", "John Doe", "Hello")


# @with_logging
async def test_create_message_rec(mock_message):
    # Call the method under test
    await create_message_rec(mock_message, 1)

    # Retrieve the created message from the database
    message = MessageModel.query.filter_by(chat_id=1).first()

    # Assert the values match
    assert message.date == "2023-07-05"
    assert message.time == "10:30"
    assert message.contact_name == "John Doe"
    assert message.text == "Hello"
    assert message.chat_id == 1


@pytest.mark.asyncio
async def test_wrapper():
    await test_create_message_rec(mock_message)
