API demo
========

This is a small web application designed to demonstrate how to use the `h.api`
package to create a Hypothesis-like JSON API for storing and retrieving
annotations.

In this example, the user list is hard-coded (see the top of `__init__.py`).
Users can request temporary API tokens (they last only as long as the server is
running), and perform operations against the API. See below for examples.

Getting started
---------------

The demo assumes you have the following installed:

- the `h` package, found in this repository
- the Pyramid web application framework
- `gunicorn`, a WSGI application server

With all these installed, you can run the application with:

    gunicorn --pythonpath path/to/contrib/ 'apidemo:create_app()'

Example usage
-------------

You can then fetch an API token by authenticating with HTTP Basic Auth to the
`/token` endpoint:

    $ curl -XPOST -u alice:s3cret http://localhost:8000/token
    {"token": "a5291f010c6ad8a743ce1dae965fc301"}

With this token, you can then use the annotations API by appending
`?token=<tokenid>` to your request. For example, to create an annotation:

    $ curl -XPOST 'http://localhost:8000/annotations?token=a5291f010c6ad8a743ce1dae965fc301' -d '{"foo": "bar"}'
    {
      "id": "AVLqo0j-1FxWup_NehDM",
      "created": "2016-02-16T16:38:11.180250+00:00",
      "updated": "2016-02-16T16:38:11.180269+00:00",
      "user": "alice",
      "group": "__world__",
      "foo": "bar",
      ...
    }
