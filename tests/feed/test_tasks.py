"""Test feed tasks."""
from deinfoxication import db
from deinfoxication.feed.tasks import update_feed
from tests.factories import FeedFactory


def test_update_feed(app):
    """Test feed update."""
    assert app
    feed = FeedFactory()
    db.session.commit()
    update_feed.apply_async((feed.id,))
    assert len(feed.articles) == 40

    update_feed.apply_async((feed.id,))
    assert len(feed.articles) == 40
