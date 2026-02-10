from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, IntegerField, EmailField, PasswordField, DateField, TimeField
from wtforms.validators import DataRequired, Optional

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField("Go to Dashboard")


class StudentForm(FlaskForm):
    full_name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    level = StringField('Level', validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[DataRequired()])
    information = TextAreaField('Information', validators=[DataRequired()])

    add = SubmitField('Add Student')