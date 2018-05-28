from application import app, db
from application.messages.models import Message
from flask import request


@app.route("/messages/new", methods=["POST"])
def messages_create():
	form = request.form
	chat_user_id = form.get("chat_user_id")
	text = form.get("text")
	msg = Message(chat_user_id, text)
	db.session.add(msg)
	db.session.commit()
	return "message posted"
