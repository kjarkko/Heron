from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from application.users.models import User


def _name_in_use(form, field):
	if not User.name_free(field.data):
		raise ValidationError('name in use')


_UVALID = [InputRequired(), Length(min=3, max=16), _name_in_use]
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
