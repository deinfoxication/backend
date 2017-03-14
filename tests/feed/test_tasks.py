"""Test feed tasks."""
import pytest
from tests.factories import FeedFactory

from deinfoxication import db
from deinfoxication.feed.tasks import update_feed


@pytest.mark.xfail(reason='Some XML error while parsing the Gnome feed; check later')
def test_update_feed(app):
    """Test feed update."""
    assert app
    feed = FeedFactory()
    db.session.commit()
    update_feed.apply_async((feed.id,))
    assert len(feed.articles) == 40

    update_feed.apply_async((feed.id,))
    assert len(feed.articles) == 40
