from flask_wtf import FlaskForm
from wtforms import validators, StringField, BooleanField, TextAreaField, SelectMultipleField


class PostForm(FlaskForm):
    title = StringField('Title', [validators.DataRequired()])
    content = TextAreaField('Content')
    categories = SelectMultipleField('Categories', coerce=int)
    published = BooleanField('Published')
