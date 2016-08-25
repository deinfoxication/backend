"""Py.test utils and fixtures."""
import urllib.parse
from functools import lru_cache

import pytest
from flask_click_migrate.commands import upgrade
from prettyconf import config
from sqlalchemy.engine import create_engine

from deinfoxication import celery, create_app, db

TEST_DB_URI = '{}_test'.format(config('SQLALCHEMY_DATABASE_URI'))


@lru_cache()
def setup_test_db(app_):
    """Setup test database."""
    import logging
    logging.basicConfig()
    engine = create_engine(app_.config['DEFAULT_DB_URI'])
    conn = engine.connect()
    url = urllib.parse.urlparse(TEST_DB_URI)
    test_db_name = url.path[1:]
    if conn.execute("SELECT COUNT(*) FROM pg_database WHERE datname = '{}'".format(
            test_db_name)).scalar() == 0:
        conn.execute('ROLLBACK')
        conn.execute('CREATE DATABASE {}'.format(test_db_name))
    conn.close()
    db.init_app(app_)
    upgrade()
    db.session.commit()


@pytest.yield_fixture()
def app():
    """Provide app to the tests."""
    app_ = create_app()
    ctx = app_.app_context()
    ctx.push()
    app_.config['DEFAULT_DB_URI'] = app_.config['SQLALCHEMY_DATABASE_URI']
    app_.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB_URI
    app_.config['CELERY_ALWAYS_EAGER'] = True

    # TODO: Check this because it could be a problem because there is only an instance of celery.
    celery.config_from_object(app_.config)
    setup_test_db(app_)

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
