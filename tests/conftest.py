"""Py.test utils and fixtures."""
import pytest

from deinfoxication import create_app


@pytest.yield_fixture()
def app():
    """Provide app to the tests."""
    app_ = create_app()
    ctx = app_.app_context()
    ctx.push()
    yield app_
    ctx.pop()


@pytest.yield_fixture()
def test_client(app):
    """Provide test client to the tests."""
    yield app.test_client()
