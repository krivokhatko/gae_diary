# -*- coding: utf-8 -*-
import logging
import datetime
import db.model
import endpoints
import jwt
import config


def token_from_user(user_db):
    jwt_secret = config.CFG_DB.jwt_secret
    if not jwt_secret:
        raise endpoints.InternalServerErrorException('JWT configuration missed.')

    payload = dict()
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=config.CFG_DB.jwt_exp_seconds)
    if config.CFG_DB.jwt_iss:
        payload['iss'] = config.CFG_DB.jwt_iss
    if config.CFG_DB.jwt_sub:
        payload['sub'] = config.CFG_DB.jwt_sub

    payload['user_email'] = user_db.email
    payload['user_id'] = user_db.key.id()

    return jwt.encode(payload, jwt_secret)


def user_from_token(token):
    jwt_secret = config.CFG_DB.jwt_secret
    if not jwt_secret:
        raise endpoints.InternalServerErrorException('JWT configuration missed.')

    try:
        payload = jwt.decode(token, jwt_secret)
        logging.info(payload)
    except jwt.InvalidTokenError:
        raise endpoints.UnauthorizedException("Token validation failed.")

    return db.model.User.get_by_id(payload.get(u'user_id'))
