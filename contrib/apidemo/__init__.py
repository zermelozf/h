# -*- coding: utf-8 -*-

"""
An example of using :py:package:`h.api` to run a standalone annotations API.

This is a small example web application, demonstrating how to use the
:py:package:`h.api` package to serve a Hypothesis-like annotations API. In this
example, the list of users is defined in a constant at the top of the file. In
a more conventional setting, developers are expected to integrate their
accounts system with the web application by way of a Pyramid Authentication
Policy.

The users defined in the USERS constant at the top of this file can request an
API token with an HTTP POST request to /token authenticated with HTTP Basic
Auth. Thereafter, they can use the token to make requests to the API by
appending

    ?token=<issuedtoken>

to their requests.

For more information about this demo application, see...
"""

import os

from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.security import Authenticated
from pyramid.settings import asbool

from . import auth

USERS = {
    'alice': 's3cret',
    'bob': 'passw0rd',
    'charlie': 'h1dden',
}


def create_app():
    settings = settings_from_environ()
    config = Configurator(settings=settings)

    config.set_authentication_policy(auth.DemoAuthenticationPolicy(USERS))
    config.set_authorization_policy(ACLAuthorizationPolicy())

    config.set_root_factory('h.api.resources.create_root')

    config.include('h.api')

    # /token view
    #
    # Make a POST request authenticated with one of the username/password pairs
    # in USERS, above, to get an API token.
    config.add_view(auth.issue_token,
                    name='token',
                    renderer='json',
                    request_method='POST',
                    effective_principals=Authenticated)

    # /whoami view
    #
    # Make a GET request to find out who the API thinks you are authenticated
    # as.
    config.add_view(lambda r: (r.authenticated_userid or '<unknown>') + '\n',
                    name='whoami',
                    renderer='string',
                    request_method='GET')

    return config.make_wsgi_app()


def settings_from_environ():
    settings_dicts = [
        _setting_str('es.host', 'ELASTICSEARCH_HOST'),
        _setting_str('es.index', 'ELASTICSEARCH_INDEX'),
        _setting_bool('pyramid.debug_all', 'DEBUG'),
    ]
    settings = {k: v
                for d in settings_dicts if d is not None
                for k, v in d.items()}
    return settings


def _setting_bool(setting, envvar):
    if envvar in os.environ:
        return {setting: asbool(os.environ[envvar])}


def _setting_str(setting, envvar):
    if envvar in os.environ:
        return {setting: os.environ[envvar]}
