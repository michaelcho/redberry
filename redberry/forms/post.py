from flask_wtf import FlaskForm
from wtforms import validators, StringField, BooleanField, TextAreaField, SelectMultipleField


class PostForm(FlaskForm):
    title = StringField('Title', [validators.DataRequired()])
    description = TextAreaField('Description')
    categories = SelectMultipleField('Categories', coerce=int)
    published = BooleanField('Published')
