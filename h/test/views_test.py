# -*- coding: utf-8 -*-
# pylint: disable=protected-access,no-self-use
from __future__ import unicode_literals

import unittest
import mock

from pyramid import exceptions
from pyramid import httpexceptions
from pyramid import testing
import pytest

from h import views


def _dummy_request():
    request = testing.DummyRequest()
    request.webassets_env = mock.MagicMock()
    request.route_url = mock.MagicMock()
    request.sentry = mock.MagicMock()
    return request


class TestAnnotationView(unittest.TestCase):

    @mock.patch('h.client.render_app_html')
    def test_og_document(self, render_app_html):
        render_app_html.return_value = '<html></html>'
        annotation = {'id': '123', 'user': 'foo'}
        annotation['document'] = {'title': 'WikiHow — How to Make a  ☆Starmap☆'}
        context = mock.MagicMock(model=annotation)
        request = _dummy_request()
        views.annotation(context, request)
        args, kwargs = render_app_html.call_args
        test = lambda d: 'foo' in d['content'] and 'Starmap' in d['content']
        assert any(test(d) for d in kwargs['extra']['meta_attrs'])

    @mock.patch('h.client.render_app_html')
    def test_og_no_document(self, render_app_html):
        render_app_html.return_value = '<html></html>'
        annotation = {'id': '123', 'user': 'foo'}
        context = mock.MagicMock(model=annotation)
        request = _dummy_request()
        views.annotation(context, request)
        args, kwargs = render_app_html.call_args
        test = lambda d: 'foo' in d['content']
        assert any(test(d) for d in kwargs['extra']['meta_attrs'])


annotator_token_fixtures = pytest.mark.usefixtures('generate_jwt', 'session')


@annotator_token_fixtures
def test_annotator_token_calls_check_csrf_token(session):
    request = testing.DummyRequest()

    views.annotator_token(request)

    session.check_csrf_token.assert_called_once_with(request,
                                                     token='assertion')


@annotator_token_fixtures
def test_annotator_token_raises_Unauthorized_if_check_csrf_token_raises(
        session):
    session.check_csrf_token.side_effect = exceptions.BadCSRFToken

    with pytest.raises(httpexceptions.HTTPUnauthorized):
        views.annotator_token(testing.DummyRequest())


@annotator_token_fixtures
def test_annotator_token_calls_generate_jwt(generate_jwt):
    request = testing.DummyRequest()

    views.annotator_token(request)

    generate_jwt.assert_called_once_with(request, 3600)


@annotator_token_fixtures
def test_annotator_token_returns_token(generate_jwt):
    request = testing.DummyRequest()

    result = views.annotator_token(request)

    assert result == generate_jwt.return_value


@pytest.fixture
def generate_jwt(request):
    patcher = mock.patch('h.views.generate_jwt', autospec=True)
    func = patcher.start()
    func.return_value = 'abc123'
    request.addfinalizer(patcher.stop)
    return func


@pytest.fixture
def session(request):
    patcher = mock.patch('h.views.session', autospec=True)
    module = patcher.start()
    request.addfinalizer(patcher.stop)
    return module
