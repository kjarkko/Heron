from application import app, db, login_required
from application.users.models import User
from application.chats.models import Chat
from application.users.forms import UserCreateForm, UserLoginForm, UsernameForm
from application.chatusers.models import ChatUser
from application.messages.models import Message
from flask import redirect, url_for, render_template, request, abort
from flask_login import login_user, logout_user, login_manager, current_user


@app.route("/users/", methods=["GET"])
@login_required()
def users_all():
	if current_user.is_admin():
		return render_template("users/all.html", users=User.query.all())
	else:
		abort(403)


@app.route("/users/new", methods=["GET", "POST"])
def users_new():
	form = UserCreateForm()
	if form.validate_on_submit():
		User.create(form.username.data, form.password.data)
		return redirect(url_for("index"))
	return render_template("users/new.html", form=form)


@app.route("/users/login", methods=["GET", "POST"])
def users_login():
	if request.method == "GET":
		return render_template("users/login.html", form=UserLoginForm())
	form = UserLoginForm(request.form)
	user = User.get(form.username.data, form.password.data)
	if not user:
		return render_template(
			"users/login.html",
			form=form,
			error="No such username or password"
		)
	login_user(user)
	return redirect(url_for("index"))


@app.route("/users/view/<user_id>/")
@login_required()
def users_view(user_id):
	user = User.find_id(user_id)
	if user is None:
		abort(404)
	chats = Chat.find_by_user(user_id)
	messages = Message.find_by_user(user_id)
	return render_template(
		"users/view.html",
		user=user,
		chats=chats,
		messages=messages
	)


@app.route("/users/logout")
def users_logout():
	logout_user()
	return redirect(url_for("index"))


@app.route("/users/edit/<user_id>", methods=["GET", "POST"])
@login_required()
def users_edit(user_id):
	form = UsernameForm()
	if form.validate_on_submit():
		current_user.set_username(form.username.data)
		return redirect(url_for("users_view", user_id=user_id))
	return render_template("users/edit.html", form=form)


@app.route("/users/delete/<user_id>", methods=["POST"])
@login_required()
def users_delete(user_id):
	if int(current_user.id) is int(user_id):
		User.delete(user_id)
		return redirect(url_for('index'))
	if current_user.is_admin():
		User.delete(user_id)
		return redirect(url_for("users_all"))
	abort(403)
