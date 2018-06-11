from application import db
from application.models import Base
from application.chatusers.models import ChatUser
from application.users.models import User
from datetime import datetime as time
from sqlalchemy.sql import text


class Message(Base):
	chat_user_id = db.Column(db.Integer, db.ForeignKey("chat_user.id"))
	text = db.Column(db.String(2048), nullable=False)

	def __init__(self, chat_user_id, text):
		self.chat_user_id = chat_user_id
		self.text = text

	def edit(self, text):
		self.text = text

	@staticmethod
	def find_all_in_chat(chat_id):
		stmt = text(
			"SELECT Account.username, Message.date_created, Message.text "
			"	FROM Message, Account "
			"LEFT JOIN Chat_user ON Chat_user.user_id = Account.id "
			"WHERE chat_user.chat_id = :chat_id "
			"	AND message.chat_user_id = chat_user.id "
			"GROUP BY message.date_created "
		).params(chat_id=chat_id)
		res = db.engine.execute(stmt)
		msg = []
		for row in res:
			msg.append({
				'name': row[0],
				'date': row[1],
				'text': row[2]
			})
		return msg


# 		return Message.query.join(ChatUser)\
# 			.filter(ChatUser.chat_id == chat_id)

	def get_user(self):
		return User.query.get(
			ChatUser.query.get(self.chat_user_id).user_id
		).username

	def get_date(self):
		return self.date_created

	def get_text(self):
		return self.text
