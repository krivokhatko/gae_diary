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
