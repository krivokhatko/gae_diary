# -*- coding: utf-8 -*-
from protorpc import messages


class UserCredentials(messages.Message):
    email = messages.StringField(1)
    password = messages.StringField(2)


class AuthToken(messages.Message):
    token = messages.StringField(1)
