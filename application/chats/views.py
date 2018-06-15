from application import app, db
from application.chats.models import Chat
from application.chats.forms import ChatForm, AddUserForm
from application.chatusers.models import ChatUser
from application.messages.models import Message
from application.messages.forms import MessageForm
from application.users.models import User
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
		ChatUser.create(current_user.id, chat.id, True)
		return redirect("/chats/" + str(chat.id))
	return render_template("/chats/new.html", form=form)


@app.route("/chats/all")
@login_required
def chats_all():
	return render_template(
		"chats/all.html",
		chats=_get_chats(current_user.id)
	)


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


@app.route("/chats/adduser/<chat_id>", methods=["POST", "GET"])
@login_required
def chats_add_user(chat_id):
	if not _admin_of(current_user.id, chat_id):
		return "not admin of chat"
	chat = Chat.query.get(chat_id)
	if not chat:
		return redirect(url_for('chats_view', chat_id=chat_id))
	form = AddUserForm()
	if form.validate_on_submit():
		user_id = User.query.filter(User.username == form.name.data)\
			.first().id
		if ChatUser.find(user_id, chat_id) is None:
			cu = ChatUser(user_id, chat_id)
			db.session.add(cu)
			db.session.commit()
		return redirect(url_for('chats_view', chat_id=chat_id))
	return render_template("/chats/adduser.html", form=form, chat=chat)


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


def _get_chats(user_id):
	return Chat.query.join(ChatUser)\
		.filter(ChatUser.user_id == user_id)\
		.all()


def _member_of(user_id, chat_id):
	return True


def _admin_of(user_id, chat_id):
	return ChatUser.find(user_id, chat_id).admin
