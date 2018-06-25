from flask import render_template
from application import app


@app.route("/")
def index(text='Welcome to Heron'):
	return render_template("index.html", text=text)
