from application import db
from sqlalchemy.orm import relationship


class ChatUser(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
	chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"), nullable=False)
	moderator = db.Column(db.Boolean(), nullable=False)
	messages = relationship('Message', cascade='delete')

	def __init__(self, user_id, chat_id, moderator=False):
		self.user_id = user_id
		self.chat_id = chat_id
		self.moderator = moderator

	def is_moderator(self):
		return self.moderator

	@staticmethod
	def delete(chat_user):
		db.session.delete(chat_user)
		db.session.commit()

	@staticmethod
	def get(cu_id):
		return ChatUser.query.get(cu_id)

	@staticmethod
	def find_by_user(user_id):
		return ChatUser.query\
			.filter_by(user_id=user_id)\
			.first()

	@staticmethod
	def find(user_id, chat_id):
		return ChatUser.query\
			.filter_by(user_id=user_id, chat_id=chat_id)\
			.first()

	@staticmethod
	def create(user_id, chat_id, moderator=False):
		cu = ChatUser(user_id, chat_id, moderator)
		db.session.add(cu)
		db.session.commit()
