from sqlalchemy.orm import synonym,foreign
from flask_sqlalchemy import SQLAlchemy
from comtoken import db
from werkzeug import check_password_hash, generate_password_hash


class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    text = db.Column(db.Text)

    def __repr__(self):
        return '<Entry id={id} title={title!r}>'.format(
                id=self.id, title=self.title)

class Gender(db.Model):
    __tablename__ = 'gender'
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Text)

    def __repr__(self):
        return '<Gender id={id}>'.format(
                id=self.id, gender=self.gender)

class House(db.Model):
    __tablename__ = 'house'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.Text)

    def __repr__(self):
        return '<house id={id}>'.format(
            id=self.id, address=self.address)


class User(db.Model):
    __tabalename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default="", nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    gender = db.Column(db.Integer)
    house = db.Column(db.Integer)
    belonging = db.Column(db.String(100))
    hobby = db.Column(db.String(100))
    profile_img = db.Column(db.String(100))
    description =db.Column(db.String(300))
    _password = db.Column('password',db.String(100))

    def _get_password(self):
        return self._password
    def _set_password(self,password):
        if password:
            password = password.strip()
        self._password = generate_password_hash(password)
    password_descriptor = property(_get_password,_set_password)
    password = synonym('_password',descriptor=password_descriptor)

    def check_password(self,password):
        password =password.strip()
        if not password:
            return False
        return check_password_hash(self.password,password)

    @classmethod
    def authenticate(cls,query,email,password):
        user = query(cls).filter(cls.email==email).first()
        if user is None:
            return None, False
        return user,user.check_password(password)

    def __repr__(self):
        return u'<User id = {self.id} email ={self.email!r}>'.format(self=self)


def init():
    db.create_all()
