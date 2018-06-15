from application import db
from application.models import Base
from sqlalchemy.sql import text


class User(Base):

	__tablename__ = "account"

	username = db.Column(db.String(16), nullable=False, unique=True)
	password = db.Column(db.String(32), nullable=False)

	def __init__(self, username, password):
		self.username = username
		self.password = password

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

	def admin_of(self, chat):
		pass

	@staticmethod
	def find_members(chat_id):
		stmt = text(
			"SELECT Account.username FROM Account "
			"LEFT JOIN Chat_user ON Chat_user.user_id = Account.id "
			"WHERE chat_user.chat_id = :chat_id "
			"ORDER BY Account.username "
		).params(chat_id=chat_id)
		res = db.engine.execute(stmt)
		users = []
		for row in res:
			users.append({
				'username': row[0]
			})
		return users

	@staticmethod
	def exists(name):
		return User.query.filter(User.username == name).first() is not None
