from application import app, db
from application.users.models import User
from application.users.forms import UserCreateForm, UserLoginForm
from flask import redirect, url_for, render_template, request
from flask_login import login_user, logout_user


@app.route("/users/", methods=["GET"])
def users_all():
	return render_template("users/all.html", users=User.query.all())


@app.route("/users/new", methods=["GET", "POST"])
def users_new():
	form = UserCreateForm()
	if form.validate_on_submit():
		usr = User(form.username.data, form.password.data)
		db.session.add(usr)
		db.session.commit()
		return redirect(url_for("index"))
	return render_template("users/new.html", form=form)


@app.route("/users/login", methods=["GET", "POST"])
def users_login():
	if request.method == "GET":
		return render_template("users/login.html", form=UserLoginForm())
	form = UserLoginForm(request.form)
	user = User.query.filter_by(
		username=form.username.data, password=form.password.data
	).first()
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
def users_delete(user_id):
	user = User.query.get(user_id)
	db.session.delete(user)
	db.session.commit()
	return redirect(url_for("users_all"))
