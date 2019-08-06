"""Worker tests."""
from deinfoxication.feed.tasks import ping


def test_ping(app):
    """Test a simple task."""
    with app.app_context():
        assert ping.apply_async().result == "pong"
