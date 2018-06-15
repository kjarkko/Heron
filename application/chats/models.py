from application import db
from application.chatusers.models import ChatUser


class Chat(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(16), nullable=False)

	def __init__(self, name):
		self.name = name

	@staticmethod
	def exists(name):
		return Chat.query.filter(Chat.name == name).first() is not None

	@staticmethod
	def find_members(chat_id):
		return db.session.query('account')\
			.join('chat_user')\
			.join('chat')\
			.filter('chat_user.chat_id' == chat_id)\
			.all()

	def is_admin(self, user_id):
		return ChatUser.find(user_id, self.id).admin
