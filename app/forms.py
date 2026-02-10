from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, IntegerField, EmailField, PasswordField, DateField, TimeField, FileField
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

class MaterialForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    material_type = SelectField(
        "Type",
        choices=[("pdf", "PDF"), ("video", "Video"), ("ppt", "PPT"), ("link", "Link")],
        validators=[DataRequired()]
    )
    file = FileField("Upload File")
    description = TextAreaField("Description")
    add = SubmitField("Add Material")