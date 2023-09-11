"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy 
import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.String(25),
                           nullable = False)
    last_name = db.Column(db.String(50),
                          nullable = False)
    image_url = db.Column(db.String)
    posts = db.relationship('Posts', backref='user', cascade='all, delete-orphan')
    #use the cascade='all, delete-orphan') basically says if this user is deleted we delete all of them
    #middleman table


    def __repr__(self):
        return f"<User(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', image_url='{self.image_url}')>"


class Posts(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    title = db.Column(db.String(), 
                      nullable = False)
    content = db.Column(db.String(),
                        nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # post_tag_post = db.relationship('PostTag', backref='posts_to_tag')
    tags = db.relationship('Tag', secondary='post_tag', back_populates='posts')

# class Tag(db.Model):
#     __tablename__ = "tags"
#     id = db.Column(db.Integer,
#                     primary_key = True,
#                     autoincrement = True)
#     tags = db.Column(db.String(),
#                     nullable = False )

#     post_tag = db.relationship('PostTag', backref='tags_for_posts')
class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    tags = db.Column(db.String(),
                    nullable=False)

    # post_tag_tag = db.relationship('PostTag', secondary='post_tag', backref='tags')
    posts = db.relationship('Posts', secondary='post_tag', back_populates='tags')

class PostTag(db.Model):
    __tablename__ = 'post_tag'
    tags_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True)

    posts_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
        #We put 2 primary keys together to say those 2 things together are primary key for PostTag


# def get_directory_join():
#     directory = db.session.query(Employee.name, Department.dept_name, Department.phone).join(Department).all()
#     for name, dept, phone in drectory:
#         print(name, dept, phone)


def connect_db(app):
    db.app = app
    db.init_app(app)