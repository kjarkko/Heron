from application import db
from datetime import datetime as time


class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	chat_user_id = db.Column(db.Integer, db.ForeignKey("chat_user.id"))
	date = db.Column(db.DateTime, default=time.utcnow)
	text = db.Column(db.String(2048), nullable=False)

	def __init__(self, chat_user_id, text):
		self.chat_user_id = chat_user_id
		self.text = text
