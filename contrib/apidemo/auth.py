# -*- coding: utf-8 -*-

import binascii
import os

from pyramid.authentication import BasicAuthAuthenticationPolicy
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.security import Everyone, Authenticated
from zope.interface import implementer

# An in-memory store for API tokens.
TOKENS = {}


@implementer(IAuthenticationPolicy)
class DemoAuthenticationPolicy(object):
    def __init__(self, users):
        self.users = users
        self.basicauth_policy = BasicAuthAuthenticationPolicy(self._check,
                                                              realm="Demo API")

    def authenticated_userid(self, request):
        if request.path.startswith('/token'):
            return self.basicauth_policy.authenticated_userid(request)
        return self._userid_from_token(request)

    def unauthenticated_userid(self, request):
        if request.path.startswith('/token'):
            return self.basicauth_policy.unauthenticated_userid(request)
        return self._userid_from_token(request)

    def effective_principals(self, request):
        principals = [Everyone]
        if request.authenticated_userid is not None:
            principals += [Authenticated, request.authenticated_userid]
        return principals

    def remember(self, request, userid, **kw):
        return []

    def forget(self, request):
        return []

    def _check(self, username, password, request):
        if self.users.get(username) == password:
            return []
        return None

    def _userid_from_token(self, request):
        try:
            token = request.params['token']
        except KeyError:
            return None
        if token not in TOKENS:
            return None
        return TOKENS[token]


def issue_token(request):
    token = binascii.hexlify(os.urandom(16))
    TOKENS[token] = request.authenticated_userid
    return {'token': token}
