import pytest
from sqlalchemy import text
from app import app, db
from db.models import UserToChats


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "sqlite:///:memory:"  # Use an in-memory SQLite database for testing
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_query(client):
    record = UserToChats(chat_name="example_chat", user_id="example_user_id")
    db.session.add(record)
    db.session.commit()

    chat_id = record.id
    sql_query = text(
        """
      SELECT contact_name, COUNT(contact_name)
      FROM messages
      WHERE contact_name IS NOT NULL AND chat_id = :chat_id
      GROUP BY contact_name
    """
    )
    result = db.session.execute(sql_query, {"chat_id": chat_id})
    assert len(result.fetchall()) == 0
