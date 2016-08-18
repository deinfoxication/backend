"""Py.test utils and fixtures."""
import pytest
from prettyconf import config

from deinfoxication import celery, create_app, db

TEST_DB_NAME = '{}_test'.format(config('SQLALCHEMY_DATABASE_URI'))


@pytest.yield_fixture()
def app():
    """Provide app to the tests."""
    app_ = create_app()
    ctx = app_.app_context()
    ctx.push()
    app_.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB_NAME
    app_.config['CELERY_ALWAYS_EAGER'] = True

    # TODO: Check this because it could be a problem because there is only an instance of celery.
    celery.config_from_object(app_.config)

    def commit():
        """Test will only flush instead of commit."""
        db.session.flush()
    old_commit = db.session.commit
    db.session.commit = commit
    yield app_
    db.session.commit = old_commit
    ctx.pop()


@pytest.yield_fixture()
def test_client(app):
    """Provide test client to the tests."""
    yield app.test_client()
