from application import db


class ChatUser(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
	chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"), nullable=False)
	admin = db.Column(db.Boolean, nullable=False)

	def __init__(self, user_id, chat_id, admin=False):
		self.user_id = user_id
		self.chat_id = chat_id
		self.admin = admin

	def find(user_id, chat_id):
		return ChatUser.query.filter_by(user_id=user_id, chat_id=chat_id).first()
