from flask import render_template,request,redirect,url_for,abort,flash,session
from flask_login import login_required
from .. request import get_quotes
from . import main
from ..models import Writer,Blog,Comment
from .forms import BlogForm,CommentForm
from .. import db

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    myquote = get_quotes()

    quote = myquote['quote']
    quote_author = myquote['author']

    return render_template('index.html',quote = quote, quote_author =  quote_author)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/blogs', methods = ['GET','POST'])
def blogs():
    blogs = Blog.query.order_by(Blog.timestamp.desc()).all()

    return render_template('blogs.html', blogs = blogs)

@main.route('/blog/<b_id>',methods = ['GET','POST'])
def oneblog(b_id):
    blog = Blog.query.filter_by(id = b_id).first()

    cform = CommentForm()
    if cform.validate_on_submit():
        newname = cform.name.data
        newcomment = cform.comment.data

        new_comment = Comment(name = newname, comment = newcomment, blog_id = b_id)

        new_comment.save_comment()
        # comments = Comment.query.filter_by(blog_id = b_id).all()

        return redirect(url_for('main.oneblog', b_id = blog.id ))

    return render_template('oneblog.html', blog = blog, comment_form = cform)

