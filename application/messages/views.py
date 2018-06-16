from application import app, db
from application.messages.models import Message
from application.messages.forms import MessageForm
from flask import request, redirect, render_template, url_for
from flask_login import login_required


@app.route("/messages/edit/<message_id>", methods=["GET", "POST"])
@login_required
def messages_edit(message_id):  # TODO validate user
	form = MessageForm()
	msg = Message.query.get(message_id)
	if form.validate_on_submit():
		msg.edit(form.text.data)
		return redirect(url_for("index"))
	return render_template("messages/edit.html", form=form, message=msg)


@app.route("/messages/delete/<message_id>", methods=["GET", "POST"])
@login_required
def messages_delete(message_id):  # TODO validate user
	Message.delete(message_id)
	return redirect(url_for("index"))
