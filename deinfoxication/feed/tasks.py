"""Feed's tasks."""
from datetime import datetime

import feedparser
import lxml
import pytz
from lxml.html import document_fromstring
from sqlalchemy.orm.exc import NoResultFound

from deinfoxication import celery, db
from deinfoxication.feed.models import Article, Feed
from deinfoxication.utils import app_context


@app_context
def update_feeds():
    """Call tasks to update each feed."""
    for feed in Feed.query.with_entities(Feed.id).all():
        update_feed.apply_async((feed.id,))


@celery.task
@app_context
def update_feed(feed_id: str) -> None:
    """Fetch a feed and apply the difference on the database."""
    feed = Feed.query.get(feed_id)
    if not feed:
        raise update_feed.retry(max_retries=1, countdown=60)  # Maybe not commited
    # Let's start the caching with etag first and then if needed we can check if other types are available
    parsed_feed = feedparser.parse(feed.url, feed.last_etag)
    if parsed_feed.status == 304:
        return
    feed.name = parsed_feed.feed.title  # Is it right to always override?
    feed.last_etag = parsed_feed.etag

    for entry in parsed_feed.entries:
        try:
            article = Article.query.filter(Article.url == entry.link).one()
        except NoResultFound:
            article = Article()
        article.feed = feed
        article.title = entry.title
        article.url = entry.link
        last_date = entry.updated_parsed if "updated_parsed" in entry else entry.published_parsed
        article.publication_date = datetime(*list(last_date)[:6], tzinfo=pytz.UTC)  # type: ignore # noqa: T484
        raw_text = entry.content[0].value if hasattr(entry, "content") else entry.summary
        article.html_text = raw_text
        try:
            doc = document_fromstring(raw_text)
            article.clean_text = doc.text_content()  # TODO: Clear an try to match up by content type
        except lxml.etree.LxmlSyntaxError:
            article.clean_text = raw_text  # FIXME: This RSS might contain XML errors
        db.session.add(article)

    db.session.commit()


@celery.task
@app_context
def ping():
    """Simple celery task."""
    return "pong"
