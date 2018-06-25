from application import app, db, login_required
from application.chats.models import Chat
from application.chats.forms import ChatForm, AddUserForm
from application.chatusers.models import ChatUser
from application.messages.models import Message
from application.messages.forms import MessageForm
from application.users.models import User
from flask import request, redirect, render_template, url_for, jsonify, abort
from flask_login import current_user, login_manager


@app.route("/chats/<chat_id>/management/add", methods=["POST"])
@login_required()
def chats_add_user(chat_id):
	if not _admin_of(current_user.id, chat_id):
		abort(403)
	form = AddUserForm(request.form)
	if form.validate():
		user_id = User.get(form.name.data).id
		if ChatUser.find(user_id, chat_id) is None:
			ChatUser.create(user_id, chat_id)
	return redirect(url_for('chats_management', chat_id=chat_id))


@app.route("/chats/new", methods=["GET", "POST"])
@login_required("ANY")
def chats_create():
	form = ChatForm()
	if form.validate_on_submit():
		chat = Chat.create(form.name.data)
		ChatUser.create(current_user.id, chat.id, True)
		return redirect("/chats/" + str(chat.id))
	return render_template("/chats/new.html", form=form)


@app.route("/chats/all")
@login_required()
def chats_all():
	if current_user.is_admin():
		return render_template(
			"chats/all.html",
			chats=Chat.all()
		)
	abort(403)


app.jinja_env.globals.update(chats_all=Chat.find_by_user)


@app.route("/chats/post/<chat_id>", methods=["POST"])
@login_required()
def chats_post(chat_id):
	if not _member_of(current_user.id, chat_id):
		abort(403)
	form = MessageForm(request.form)
	Message.create(
		ChatUser.find(current_user.id, chat_id).id,
		form.text.data
	)
	return redirect("/chats/" + chat_id)


@app.route("/chats/<chat_id>/", methods=["GET"])
@login_required()
def chats_view(chat_id):
	if not _member_of(current_user.id, chat_id):
		abort(403)
	chat = Chat.get(chat_id)
	if not chat:
		return redirect(url_for('chats_all'))
	return render_template(
		"chats/view.html",
		chat=chat,
		messages=Message.find_all_in_chat(chat_id),
		form=MessageForm()
	)


@app.route("/chats/_m/")
@login_required()
def chats_get_messages():
	chat_id = request.args.get('chat_id', 0, type=int)
	if not _member_of(current_user.id, chat_id):
		abort(403)
	return jsonify(
		messages=render_template(
			'messages/messages.html',
			messages=Message.find_all_in_chat(chat_id)
		)
	)


@app.route("/chats/<chat_id>/management")
@login_required()
def chats_management(chat_id):
	if not _member_of(current_user.id, chat_id):
		abort(403)
	chat = Chat.get(chat_id)
	users = User.find_members(chat_id)
	return render_template(
		"chats/management.html",
		users=users,
		chat=chat,
		form=AddUserForm()
	)


@app.route("/chats/delete/<chat_id>", methods=["POST"])
@login_required()
def chats_delete(chat_id):
	if not current_user.is_admin():
		abort(403)
	Chat.delete(chat_id)
	return redirect(url_for('chats_all'))


@app.route("/chats/<chat_id>/management/delete/<user_id>", methods=["POST"])
@login_required()
def chats_delete_user(chat_id, user_id):
	if not _admin_of(current_user.id, chat_id):
		abort(403)
	cu = ChatUser.find(user_id, chat_id)
	if cu is not None:
		ChatUser.delete(cu)
	return redirect(url_for('chats_management', chat_id=chat_id))


def _member_of(user_id, chat_id):
	return ChatUser.find(user_id, chat_id) is not None


def _admin_of(user_id, chat_id):
	cu = ChatUser.find(user_id, chat_id)
	return cu.is_moderator()
