from datetime import datetime

from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import db
from flask_login import UserMixin

song_user = db.Table('song_user', db.Model.metadata,
                     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                     db.Column('song_id', db.Integer, db.ForeignKey('songs.id')))

class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=True, unique=False)
    artist = db.Column(db.String(300), nullable=True, unique=False)
    year = db.Column(db.String(50), nullable=True, unique=False)
    genre = db.Column(db.String(300), nullable=True, unique=False)

    def __init__(self, title, artist, year, genre):
        self.title = title
        self.artist = artist
        self.year = year
        self.genre = genre


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False, unique=True)
    about = db.Column(db.String(300), nullable=True, unique=False)
    authenticated = db.Column(db.Boolean, default=False)
    registered_on = db.Column('registered_on', db.DateTime)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    is_admin = db.Column('is_admin', db.Boolean(), nullable=False, server_default='0')
    # songs = db.relationship("Song", back_populates="user", cascade="all, delete")
    songs = db.relationship("Song", secondary=song_user, backref="users")

    # `roles` and `groups` are reserved words that *must* be defined
    # on the `User` model to use group- or role-based authorization.

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.email
