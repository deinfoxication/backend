"""Test feed tasks."""
from deinfoxication import db
from deinfoxication.feed.tasks import update_feed
from tests.factories import FeedFactory


def test_update_feed(app):
    """Test feed update."""
    feed = FeedFactory()
    db.session.commit()
    update_feed(feed.id)
    assert len(feed.articles) == 1022
