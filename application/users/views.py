from application import app, db
from application.users.models import User
from flask import redirect, url_for, render_template, request


@app.route("/users/", methods=["GET"])
def users_all():
	return render_template("users/all.html", users=User.query.all())


@app.route("/users/new")
def users_form():
	return render_template("users/new.html")


@app.route("/users/", methods=["POST"])
def users_create():
	form = request.form
	usr = User(form.get("username"), form.get("password"))
	db.session.add(usr)
	db.session.commit()
	return redirect(url_for("users_all"))


@app.route("/users/delete/<user_id>", methods=["POST"])
def users_delete(user_id):
	user = User.query.get(user_id)
	db.session.delete(user)
	db.session.commit()
	return redirect(url_for("users_all"))
