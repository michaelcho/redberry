from flask_wtf import FlaskForm
from wtforms import validators, StringField, BooleanField, TextAreaField, SelectMultipleField


class PostForm(FlaskForm):
    title = StringField('Title', [validators.DataRequired()])
    summary = TextAreaField('Summary')
    content = TextAreaField('Content')
    hero_image = StringField('Hero Image')
    categories = SelectMultipleField('Categories', coerce=int)
    published = BooleanField('Published')
