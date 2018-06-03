from application import app, db
from application.chatusers.models import ChatUser
from application.chatusers.forms import ChatUserForm
from flask import request, redirect
from flask_login import login_required, current_user


def _is_admin(user_id, chat_id):
	return True


"""
@app.route("/chatusers/new/", methods=["POST"])
@login_required
def chatusers_create():
	if not _is_admin(current_user.id, form.chat_id.data):
		return "not admin"

	form = ChatUserForm(request.form)
	cu = ChatUser(
		user_id=form.user_id.data,
		chat_id=form.chat_id.data,
		admin=form.admin.data
	)
	db.session.add(cu)
	db.session.commit()
	return redirect('/chats/%d'.format(chat_id))
"""
