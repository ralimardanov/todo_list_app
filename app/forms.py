from wtforms import SubmitField, StringField, PasswordField,DateTimeField,DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf import FlaskForm

class SignUpForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired(),Length(min=2,max=255)])
    surname = StringField("Surname",validators=[DataRequired(),Length(min=2,max=255)])
    email = StringField("Email",validators=[Email(message="Enter valid email address"),DataRequired()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=3,max=123)])
    password2 = PasswordField("Confirm Password",validators=[EqualTo("password"),DataRequired()])
    submit = SubmitField("submit")

class LoginForm(FlaskForm):
    email = StringField("Email",validators=[Email(message="Enter valid email address"),DataRequired()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=3,max=123)])
    submit = SubmitField('Log In')

class PassChangeForm(FlaskForm):
    email = StringField("Email",validators=[Email(message="Enter valid email address"),DataRequired()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=3,max=123)])
    password2 = PasswordField("Confirm Password",validators=[EqualTo("password"),DataRequired()])
    submit = SubmitField('submit')
class TodoForm(FlaskForm):
    date = DateField("Todo date",validators=[DataRequired()])
    whattodo = StringField("Yout Todo",validators=[DataRequired(),Length(min=5,max=350)])