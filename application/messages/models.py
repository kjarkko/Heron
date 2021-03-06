from application import db
from application.models import Base
import datetime
from sqlalchemy.sql import text


class Message(Base):
	chat_user_id = db.Column(db.Integer, db.ForeignKey("chat_user.id"))
	text = db.Column(db.String(2048), nullable=False)

	def __init__(self, chat_user_id, text):
		self.chat_user_id = chat_user_id
		self.text = text

	def edit(self, text):
		self.text = text
		db.session.commit()

	@staticmethod
	def create(chat_user_id, text):
		msg = Message(chat_user_id, text)
		db.session.add(msg)
		db.session.commit()
		return msg

	@staticmethod
	def delete(message_id):
		db.session.delete(Message.query.get(message_id))
		db.session.commit()

	@staticmethod
	def get(message_id):
		return Message.query.get(message_id)

	@staticmethod
	def find_by_user(user_id):
		stmt = text(
			"SELECT Message.date_created, Message.date_modified, Message.text "
			"	FROM Message "
			"LEFT JOIN Chat_user ON Chat_user.id = Message.chat_user_id "
			"WHERE Chat_user.user_id = :user_id "
			"ORDER BY Message.date_created "
		).params(user_id=user_id)
		res = db.engine.execute(stmt)
		msg = []
		for row in res:
			msg.append({
				'date_created': row[0],
				'date_modified': row[1],
				'text': row[2]
			})
		return msg

	@staticmethod
	def find_all_in_chat(chat_id, after=0):
		stmt = text(
			"SELECT Account.username, Message.date_created, Message.text, Message.id "
			"	FROM Message, Account "
			"LEFT JOIN Chat_user ON Chat_user.user_id = Account.id "
			"WHERE (chat_user.chat_id = :chat_id "
			"	AND Message.chat_user_id = Chat_user.id "
			"	AND Message.id > :after) "
			"ORDER BY Message.date_created "
		).params(chat_id=chat_id, after=after)
		res = db.engine.execute(stmt)
		msg = []
		for row in res:
			msg.append({
				'name': row[0],
				'date': row[1],
				'text': row[2],
				'id': row[3]
			})
		return msg
