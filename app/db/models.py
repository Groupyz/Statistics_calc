from app import db


class UserToChats(db.Model):
    __tablename__ = "user_to_chats"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_name = db.Column(db.String(255))
    user_id = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"UserToChats(id={self.id}, chat_name='{self.chat_name}', user_id='{self.user_id}')"


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(255))
    time = db.Column(db.String(255))
    contact_name = db.Column(db.String(255))
    text = db.Column(db.String(255))
    chat_id = db.Column(db.Integer, db.ForeignKey("user_to_chats.id"))

    def __repr__(self):
        return (
            f"Message(id={self.id}, date='{self.date}', time='{self.time}', "
            f"contact_name='{self.contact_name}', text='{self.text}', chat_id={self.chat_id})"
        )


# chat_id = 123
# sql_query = '''
#     SELECT contact_name, COUNT(contact_name)
#     FROM Message
#     WHERE contact_name IS NOT NULL AND chat_id =: chat_id
#     GROUP BY contact_name
# '''

# result = db.session.execute(sql_query, {"chat_id": chat_id})
# Create view Contant_to_amount as (
# 	Select contact_name, count(contact_name)
# 	From Message
# 	Where contact_name != null AND chat_id = chat_id
# 	Group by (contact_name)
# )

# Make time rounded to last hour & than
# Create view time_to_amount as (
# 	Select time, count(time) // rounded time!!
# 	FROM Message // after time changed
# 	Where time != null
# 	Group by (time)
# )
