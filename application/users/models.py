from application import db

_CTIME = db.func.current_timestamp


class User(db.Model):

	__tablename__ = "account"

	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=_CTIME())
	date_modified = db.Column(db.DateTime, default=_CTIME(), onupdate=_CTIME())
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
