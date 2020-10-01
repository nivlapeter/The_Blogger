from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
from sqlalchemy import desc

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(writer_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure = db.Column(db.String(255))

    writer_id = db.Column(db.Integer, db.ForeignKey('writer.id'))       #one writer is shared by many users
    
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
            self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):     #makes it easier to debug our applications.
        return f'User {self.username}'

class Writer(UserMixin,db.Model):
    __tablename__ = 'writer'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure = db.Column(db.String(255))

    users = db.relationship('User',backref = 'writer',lazy="dynamic")     #db.relationship to create a virtual column that will connect with the foreign key
    blogs = db.relationship('Blog',backref = 'writer',lazy="dynamic")
    
class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255))
    blog = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))        #one writer is shared by many blogs
   
    comments = db.relationship('Comment', backref='blog', lazy='dynamic')       #creating a virtual column to connect with the foreign key. It will help in displaying comments per blog

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_blogs(cls,id):
        blogs = Blog.query.filter_by(blog_id=id).all()
        return blogs

    #get the new blogs
    @classmethod
    def get_newblogs(cls):

        blog = Blogs.query.order_by(desc(Blogs.id)).filter_by(deleted=False).limit(5)
#        blog = Blogs.select().order_by(Blogs.c.id.desc())

        return blog

    #get blog according to id
    @classmethod
    def get_singleblog(cls,id):
        blogs = Blogs.query.filter_by(id=id).first()
        return blogs

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    comment = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))      #one user has many comments
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))      #one blog has many comments
    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()
    
    
    #get comments according to  pitchid
    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(blog_id=id).filter_by(deleted=False).all()
        return comments

    #get blog according to id
    @classmethod
    def get_singcomment(cls,id):
        com = Comment.query.filter_by(id=id).first()
        return com

class Quotes:
    '''
    quotes class to define quotes Objects
    '''

    def __init__(self,id,author,quote):
        self.id =id
        self.author = author
        self.quote = quote