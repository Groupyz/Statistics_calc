import pytest
from app import app, db, logger
from logger import with_logging
from db.models import UserToChats, Message
from statistics import Statistics

DUMMY_CHAT_NAME = "example_chat"


@with_logging
def create_dummy_message(**kwargs) -> Message:
    message = Message(
        date="2023-07-05", time="10:30", contact_name="John Doe", text="Hello"
    )
    for key, value in kwargs.items():
        setattr(message, key, value)

    return message


@pytest.fixture(scope="module")
def start_app_and_db():
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


@pytest.fixture(scope="module")
def db_session(start_app_and_db):
    chat = UserToChats(chat_name=DUMMY_CHAT_NAME, user_id="example_user_id")
    db.session.add(chat)
    db.session.commit()
    jhon1 = create_dummy_message(contact_name="John Doe", chat_id=chat.id)
    jhon2 = create_dummy_message(contact_name="John Doe", chat_id=chat.id)
    michi1 = create_dummy_message(contact_name="Michi Pug", chat_id=chat.id)
    records = [jhon1, jhon2, michi1]
    db.session.add_all(records)
    db.session.commit()

    return chat, jhon1, jhon2, michi1


@with_logging
def test_chat_macro_detail(db_session):
    chat, jhon1, jhon2, michi1 = db_session
    statistics = Statistics(chat.id)
    macro_detail = statistics.macro_details

    assert macro_detail.name == DUMMY_CHAT_NAME
    assert macro_detail.num_of_messages == 3


@with_logging
def test_chat_micro_detail(db_session):
    try:
        chat, jhon1, jhon2, michi1 = db_session
        statistics = Statistics(chat.id)
        micro_detail = statistics.micro_details.name_to_num_of_messages

        assert micro_detail["John Doe"] == 2
        assert micro_detail["Michi Pug"] == 1
    except Exception as e:
        logger.error(e)
        raise e
