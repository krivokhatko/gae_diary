# -*- coding: utf-8 -*-
import endpoints
from protorpc import remote

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
        # TODO: JWT token
        token = request.email + ':' + request.password
        return message.AuthToken(token=token)
