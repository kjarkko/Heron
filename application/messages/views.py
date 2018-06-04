from application import app, db
from application.messages.models import Message
from application.messages.forms import MessageForm
from flask import request, redirect, render_template, url_for
from flask_login import login_required


@app.route("/messages/new", methods=["POST"])  # TODO: not in use
def messages_create():
	form = request.form
	chat_user_id = form.get("chat_user_id")
	text = form.get("text")
	msg = Message(chat_user_id, text)
	db.session.add(msg)
	db.session.commit()
	return "message posted"


@app.route("/messages/edit/<message_id>", methods=["GET", "POST"])
@login_required
def messages_edit(message_id):  # TODO validate user
	form = MessageForm()
	msg = Message.query.get(message_id)
	if form.validate_on_submit():
		msg.text = form.text.data
		db.session.commit()
		return redirect(url_for("index"))
	return render_template("messages/edit.html", form=form, message=msg)


@app.route("/messages/delete/<message_id>", methods=["GET", "POST"])
@login_required
def messages_delete(message_id):  # TODO validate user
	db.session.delete(Message.query.get(message_id))
	db.session.commit()
	return redirect(url_for("index"))
