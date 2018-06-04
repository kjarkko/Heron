from application import db
from application.chatusers.models import ChatUser
from application.users.models import User
from datetime import datetime as time


class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	chat_user_id = db.Column(db.Integer, db.ForeignKey("chat_user.id"))
	date = db.Column(db.DateTime, default=time.utcnow)
	text = db.Column(db.String(2048), nullable=False)

	def __init__(self, chat_user_id, text):
		self.chat_user_id = chat_user_id
		self.text = text

	def find_all_in_chat(chat_id):  # TODO ignores id and fetches all messages
		return Message.query.join(ChatUser, ChatUser.chat_id == chat_id)\
			.all()

	def get_user(self):
		return User.query.get(
			ChatUser.query.get(self.chat_user_id).user_id
		).username

	def get_date(self):
		return self.date.ctime()

	def get_text(self):
		return self.text
