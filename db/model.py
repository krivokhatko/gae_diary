# -*- coding: utf-8 -*-
from google.appengine.ext import ndb


class User(ndb.Model):
    email = ndb.StringProperty(indexed=True)
    password_hash = ndb.StringProperty()

    @classmethod
    def get_by_email(cls, email):
        return cls.query().filter(cls.email == email).get()


class Record(ndb.Model):
    user = ndb.KeyProperty(kind=User)
    created = ndb.DateTimeProperty(auto_now_add=True)
    notes = ndb.TextProperty()


class Config(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)
    jwt_secret = ndb.StringProperty(default='')
    jwt_exp_seconds = ndb.IntegerProperty(default=3600)
    jwt_iss = ndb.StringProperty(default='')
    jwt_sub = ndb.StringProperty(default='')

    @classmethod
    def get_primary_db(cls):
        return cls.get_or_insert('primary')

