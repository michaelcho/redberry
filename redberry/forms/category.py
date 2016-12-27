from flask_wtf import FlaskForm
from wtforms import validators, StringField, TextAreaField


class CategoryForm(FlaskForm):
    title = StringField('Title', [validators.DataRequired()])
    description = TextAreaField('Description')
