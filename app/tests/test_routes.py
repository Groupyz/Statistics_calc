import pytest
import os
from app import app, db, logger
from logger import with_logging
from db.models import UserToChats, Message
from tests.test_statistics import create_dummy_message


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "sqlite:///:memory:"  # Use an in-memory SQLite database for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


def create_valid_txt_file():
    file_path = "valid.txt"
    with open(file_path, "w") as file:
        lines = [
            "11/21/22, 22:16 - Omer LeiBo: לא הוא עוד לא ענה, שלחתי לו אתמול עוד תזכורת במייל אבל מחר אני כבר אשלח לו הודעה",
            "11/21/22, 22:21 - Ns: חיה, תודה👌🏿",
        ]
        for line in lines:
            file.write(line + "\n")


def remove_valid_txt_file():
    file_path = "valid.txt"
    os.remove(file_path)


@pytest.fixture(autouse=True)
def setup_teardown():
    create_valid_txt_file()
    yield
    remove_valid_txt_file()


@with_logging
def test_upload_text_stream(client):
    data = {
        "file": (open("valid.txt", "rb"), "valid.txt"),
        "user_id": "your_user_id_value",
    }

    response = client.post("/createChat", data=data, content_type="multipart/form-data")
    assert response.status_code == 201


@with_logging
def test_get_statistics_valid(client):
    try:
        record = create_user_to_chat_record()
        create_message_connected_to(record.id)
        response = client.get("/statistics/{}".format(record.id))
        assert response.status_code == 200
    except Exception as e:
        logger.error(e)
        raise e


@with_logging
def test_get_statistics_unvalid(client):
    record = create_user_to_chat_record()
    id = record.id
    db.session.delete(record)
    db.session.commit()
    response = client.get("/statistics/{}".format(id))

    assert response.status_code == 400


def create_user_to_chat_record() -> UserToChats:
    record = UserToChats(chat_name="example_chat", user_id="example_user_id")
    db.session.add(record)
    db.session.commit()
    return record


def create_message_connected_to(chat_id: int) -> Message:
    message = create_dummy_message(chat_id=chat_id)
    db.session.add(message)
    db.session.commit()
    return message
