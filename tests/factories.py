"""Model's factories."""
import factory
from factory.alchemy import SQLAlchemyModelFactory

from deinfoxication import db
from deinfoxication.feed.models import Article, Feed


class FeedFactory(SQLAlchemyModelFactory):
    """Feed's factory."""

    name = 'Gnome Planet'
    url = 'http://planet.gnome.org/atom.xml'

    class Meta:
        """Factory's configurations."""

        model = Feed
        sqlalchemy_session = db.session


class ArticleFactory(SQLAlchemyModelFactory):
    """Article's factory."""

    feed = factory.SubFactory(FeedFactory)

    title = 'An Article'
    url = 'article-url'

    class Meta:
        """Factory's configurations."""

        model = Article
        sqlalchemy_session = db.session
