from application import db
from application.chatusers.models import ChatUser


class Chat(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(16), nullable=False)

	def __init__(self, name):
		self.name = name

	@staticmethod
	def all():
		return Chat.query.all()

	@staticmethod
	def get(chat_id):
		return Chat.query.get(chat_id)

	@staticmethod
	def find_by_user(user_id):
		return Chat.query.join(ChatUser)\
			.filter(ChatUser.user_id == user_id)\
			.all()

	@staticmethod
	def create(name):
		chat = Chat(name)
		db.session.add(chat)
		db.session.commit()
		return chat

	@staticmethod
	def exists(name):
		return Chat.query.filter(Chat.name == name).first() is not None

	def is_admin(self, user_id):
		return ChatUser.find(user_id, self.id).is_moderator()
