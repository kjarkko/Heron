from application import app, db
from application.chats.models import Chat
from flask import request, redirect


@app.route("/chats/new", methods=["POST"])
def chats_create():
	form = request.form
	chat = Chat(form.get("chat_name"))
	db.session.add(chat)
	db.session.commit()
	return redirect("/chats/" + chat.id)


@app.route("/chats/<chat_id>/", methods=["POST"])
def chat_post(chat_id):
	# chat = Chat.query.get(chat_id)
	return ""


@app.route("/chats/<chat_id>/", methods=["GET"])
def chat_view(chat_id):
	# chat = Chat.query.get(chat_id)
	return ""
