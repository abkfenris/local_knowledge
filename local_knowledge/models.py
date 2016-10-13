from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from geoalchemy2 import Geometry
from sqlalchemy.dialects import postgresql

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username


class Node(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    osm_id = db.Column(db.BigInteger(), index=True, unique=True)
    geom = db.Column(Geometry('POINT', 4326))
    json = db.Column(postgresql.JSONB)
    created = db.Column(db.DateTime())
    updated = db.Column(db.DateTime())


class Way(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    osm_id = db.Column(db.BigInteger(), index=True, unique=True)
    geom = db.Column(Geometry('LINESTRING', 4326))
    name = db.Column(db.String())
    json = db.Column(postgresql.JSONB)
    created = db.Column(db.DateTime())
    updated = db.Column(db.DateTime())
