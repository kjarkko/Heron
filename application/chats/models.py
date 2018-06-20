from application import db
from application.chatusers.models import ChatUser
from application.messages.models import Message
from application.users.models import User


class Chat(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(16), nullable=False)

	def __init__(self, name):
		self.name = name

	@staticmethod
	def delete(chat_id):
		chat = Chat.get(chat_id)
		db.session.delete(chat)
		db.session.commit()

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

	def is_admin(self, user_id):  # TODO refactor into is_moderator
		return ChatUser.find(user_id, self.id).is_moderator()

	def can_edit(self, user_id, message_id):
		cu = ChatUser.find(user_id, self.id)
		return cu.id == Message.get(message_id).chat_user_id

	def can_delete(self, user_id, message_id):
		if self.is_admin(user_id):
			return True
		user = User.find_id(user_id)
		if user.is_admin():
			return True
		cu = ChatUser.find(user_id, self.id)
		return cu.id == Message.get(message_id).chat_user_id
