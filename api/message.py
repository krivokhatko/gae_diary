# -*- coding: utf-8 -*-
from protorpc import messages
from protorpc import message_types


class UserCredentials(messages.Message):
    email = messages.StringField(1, required=True)
    password = messages.StringField(2, required=True)


class AuthToken(messages.Message):
    token = messages.StringField(1)


class DiaryRecord(messages.Message):
    notes = messages.StringField(1, required=True)
    created = message_types.DateTimeField(2)


class DiaryRecordCollection(messages.Message):
    items = messages.MessageField(DiaryRecord, 1, repeated=True)
