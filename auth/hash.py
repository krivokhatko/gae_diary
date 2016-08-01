# -*- coding: utf-8 -*-

from passlib.hash import pbkdf2_sha512


def password_encrypt(password):
    pass_hash = pbkdf2_sha512.encrypt(password, rounds=2000, salt_size=16)
    return pass_hash


def password_verify(password, password_hash):
    return pbkdf2_sha512.verify(password, password_hash)
