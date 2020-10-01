from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import InputRequired,Length

class BlogForm(FlaskForm):
    title= StringField('Blog Title',validators=[InputRequired()], render_kw={"placeholder": "Enter your blog title"})
    blog= TextAreaField('Input your blog', validators=[InputRequired()], render_kw={"placeholder": "Post your blog"})
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    name = StringField('', validators=[InputRequired()], render_kw={"placeholder": "Enter your name"})
    comment = StringField('', validators=[InputRequired()], render_kw={"placeholder": "Post your comment"})
    submit = SubmitField('Post')

