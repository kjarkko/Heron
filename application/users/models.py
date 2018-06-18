from application import db
from application.models import Base
from application.chatusers.models import ChatUser
from application.messages.models import Message
from sqlalchemy.sql import text
from sqlalchemy.types import Boolean


class User(Base):

	__tablename__ = "account"

	username = db.Column(db.String(16), nullable=False, unique=True)
	password = db.Column(db.String(32), nullable=False)
	admin = db.column(db.String(8))  # TODO fix bool

	def __init__(self, username, password, admin=False):
		self.username = username
		self.password = password
		self.admin = 'ADMIN' if admin is True else 'USER'

	def roles(self, chat_id=None, msg_id=None):
		roles = []
		if self.admin is True:
			roles.append('ADMIN')
		if chat_id is not None:
			cu = ChatUser.find(self.id, chat_id)
			if cu is not None:
				roles.append('MEMBER')
				if cu.moderator:
					roles.append('MODERATOR')
		if msg_id is not None:
			cu = ChatUser.get(Message.get(msg_id).chat_user_id)
			if cu.user_id == self.id:
				roles.append('POSTER')
		return roles

	def is_admin(self):
		return self.admin == 'ADMIN'

	def get_id(self):
		return self.id

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def is_authenticated(self):
		return True

	def find_all_chats(self):
		pass

	def moderator_of(self, chat_id):
		return ChatUser.find(self.id, chat_id).moderator

	@staticmethod
	def create(username, password):
		u = User(username, password)
		db.session.add(u)
		db.session.commit()
		return u

	@staticmethod
	def delete(user_id):
		user = User.query.get(user_id)
		db.session.delete(user)
		db.session.commit()

	@staticmethod
	def get(username, password=None):
		if password is not None:
			return User.query.filter(
				User.username == username,
				User.password == password
			).first()
		else:
			return User.query.filter(
				User.username == username
			).first()

	@staticmethod
	def find_members(chat_id):
		stmt = text(
			"SELECT Account.username, Account.id FROM Account "
			"LEFT JOIN Chat_user ON Chat_user.user_id = Account.id "
			"WHERE chat_user.chat_id = :chat_id "
			"ORDER BY Account.username "
		).params(chat_id=chat_id)
		res = db.engine.execute(stmt)
		users = []
		for row in res:
			users.append({
				'username': row[0],
				'id': row[1]
			})
		return users

	@staticmethod
	def exists(username, password=None):
		if password is None:
			return User.query\
				.filter(User.username == username)\
				.first() is not None
		else:
			return User.query\
				.filter(User.username == username, User.password == password)\
				.first() is not None
