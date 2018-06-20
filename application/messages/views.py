from application import app, db
from application.messages.models import Message
from application.messages.forms import MessageForm
from application.chatusers.models import ChatUser
from flask import request, redirect, render_template, url_for, abort
from flask_login import login_required, current_user


@app.route("/messages/edit/<message_id>", methods=["GET", "POST"])
@login_required
def messages_edit(message_id):
	if not _is_sender(message_id):
		return "not sender"

	form = MessageForm()
	msg = Message.get(message_id)
	if form.validate_on_submit():
		msg.edit(form.text.data)
		return redirect(url_for("index"))
	return render_template("messages/edit.html", form=form, message=msg)


@app.route("/messages/delete/<message_id>", methods=["GET", "POST"])
@login_required
def messages_delete(message_id):
	if not _is_auth(message_id):
		abort(403)
	msg = Message.get(message_id)
	chat_id = ChatUser.get(msg.chat_user_id).chat_id
	Message.delete(message_id)
	return redirect(url_for("chats_view", chat_id=chat_id))


def _is_auth(message_id):
	if current_user.is_admin():
		return True
	if _is_sender(message_id):
		return True
	if _is_moderator(message_id):
		return True
	return False


def _is_sender(msg_id):
	sender_cu = ChatUser.get(Message.get(msg_id).chat_user_id)
	chat_id = sender_cu.chat_id
	editor_cu = ChatUser.find(current_user.id, chat_id)
	return sender_cu.id is editor_cu.id


def _is_moderator(message_id):
	cu_id = Message.get(message_id).chat_user_id
	return ChatUser.get(cu_id).is_moderator()
