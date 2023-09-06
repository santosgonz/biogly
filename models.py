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



def connect_db(app):
    db.app = app
    db.init_app(app)