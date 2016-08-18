"""Feed's tasks."""
from deinfoxication import celery
from deinfoxication.feed.models import Feed
from deinfoxication.utils import app_context


@app_context
def update_feeds():
    """Call tasks to update each feed."""
    for feed in Feed.query.with_entities(Feed.id).all():
        update_feed.apply_async((feed.id,))


@app_context
def update_feed():
    """Fetch a feed and apply the difference on the database."""
    pass


@celery.task
@app_context
def ping():
    """Simple celery task."""
    return 'pong'
