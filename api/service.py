# -*- coding: utf-8 -*-
import logging
import endpoints
from protorpc import remote
from protorpc import message_types
import auth
import db.model
import message


@endpoints.api(name='user', version='v1')
class UsersApi(remote.Service):
    @endpoints.method(
        message.UserCredentials,
        message.AuthToken,
        path='token',
        http_method='POST',
        name='user.token')
    def token_user(self, request):
        user = db.model.User.get_by_email(request.email)
        if user and auth.password_verify(request.password, user.password_hash):
            token = auth.token_from_user(user)
        else:
            raise endpoints.UnauthorizedException('Wrong user.')

        return message.AuthToken(token=token)


@endpoints.api(name='diary', version='v1')
class DiaryApi(remote.Service):
    @classmethod
    def authenticate(cls, request_state):
        token = None
        user = None
        auth_value = request_state.headers.get(u'Authorization', '').split()
        if auth_value and auth_value[0].lower() == b'bearer' and len(auth_value) == 2:
            token = auth_value[1]
            user = auth.user_from_token(token)
        else:
            raise endpoints.UnauthorizedException('Token missed')

        return user, token

    @endpoints.method(
        message.DiaryRecord,
        message_types.VoidMessage,
        path='add',
        http_method='POST',
        name='record.add')
    def add_record(self, request):
        user = db.model.User.get_by_email('user0@email.com')
        if user:
            record = db.model.Record(user=user.key, notes=request.notes)
            record.put()

        return message_types.VoidMessage()

    @endpoints.method(
        message_types.VoidMessage,
        message.DiaryRecordCollection,
        path='list',
        http_method='GET',
        name='record.list')
    def list_record(self, request):
        user = db.model.User.get_by_email('user0@email.com')
        if user:
            msg_records = list()
            records = db.model.Record.query_records(user.key)
            for rec in records:
                msg_records.append(message.DiaryRecord(notes=rec.notes, created=rec.created))
            return message.DiaryRecordCollection(items=msg_records)
