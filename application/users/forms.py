from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo

_UVALID = [InputRequired(), Length(min=3, max=16)]
_PVALID = [
	InputRequired(),
	Length(min=5, max=32),
	EqualTo("confirm", message="passwords must match")
]


class UserCreateForm(FlaskForm):
	username = StringField("Username", _UVALID)
	password = PasswordField("Password", _PVALID)
	confirm = PasswordField("Repeat password")

	class Meta:
		csrf = False


class UserLoginForm(FlaskForm):
	username = StringField("Username")
	password = PasswordField("Password")

	class Meta:
		csrf = False
