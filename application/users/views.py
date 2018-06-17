from application import app, db, login_required
from application.users.models import User
from application.users.forms import UserCreateForm, UserLoginForm
from flask import redirect, url_for, render_template, request
from flask_login import login_user, logout_user, login_manager, current_user


@app.route("/users/", methods=["GET"])
@login_required()
def users_all():
	if current_user.is_admin():
		return render_template("users/all.html", users=User.query.all())
	else:
		return login_manager.unauthorized()


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


@app.route("/users/logout")
def users_logout():
	logout_user()
	return redirect(url_for("index"))


@app.route("/users/delete/<user_id>", methods=["POST"])
@login_required(role="ADMIN")
def users_delete(user_id):
	User.delete(user_id)
	return redirect(url_for("users_all"))
