from application import db
from application.models import Base

_CTIME = db.func.current_timestamp


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
