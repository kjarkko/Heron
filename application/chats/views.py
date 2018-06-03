from application import app, db
from application.chats.models import Chat
from application.chats.forms import ChatForm
from application.chatusers.models import ChatUser
from application.messages.models import Message
from application.messages.forms import MessageForm
from flask import request, redirect, render_template, url_for
from flask_login import login_required, current_user


@app.route("/chats/new", methods=["GET", "POST"])
@login_required
def chats_create():
	form = ChatForm()
	if form.validate_on_submit():
		chat = Chat(form.name.data)
		db.session.add(chat)
		db.session.commit()
		chat_user = ChatUser(current_user.id, chat.id, True)
		db.session.add(chat_user)
		db.session.commit()
		return redirect("/chats/" + str(chat.id))
	return render_template("/chats/new.html", form=form)


@app.route("/chats/all")
@login_required
def chats_all():
	return "TODO"


@app.route("/chats/post/<chat_id>", methods=["POST"])
@login_required
def chats_post(chat_id):
	if not _member_of(current_user.id, chat_id):
		return "not member of chat"
	form = MessageForm(request.form)
	msg = Message(ChatUser.find(current_user.id, chat_id).id, form.text.data)
	db.session.add(msg)
	db.session.commit()
	return redirect("/chats/" + chat_id)


@app.route("/chats/<chat_id>/", methods=["GET"])
@login_required
def chats_view(chat_id):
	if not _member_of(current_user.id, chat_id):
		return "not member of chat"
	chat = Chat.query.get(chat_id)
	if not chat:
		return redirect(url_for('chats_all'))
	return render_template(
		"chats/view.html",
		chat=chat,
		messages=Message.find_all_in_chat(chat_id),
		form=MessageForm()
	)


def _member_of(user_id, chat_id):
	return True
