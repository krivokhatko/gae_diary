# -*- coding: utf-8 -*-
import endpoints
from protorpc import remote
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
