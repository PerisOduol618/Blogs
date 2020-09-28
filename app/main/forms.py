from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Bio.',validators = [Required()])
    submit = SubmitField('Submit')


class BlogForm(FlaskForm):
    title_blog = StringField('Title')
    description = TextAreaField('Write a Description', validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('Write a comment', validators=[Required()])
    submit = SubmitField('Comment')


