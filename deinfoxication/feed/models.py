"""User's models."""
from sqlalchemy.dialects import postgresql

from deinfoxication import db


class User(db.Model):
    """User model."""

    id = db.Column(postgresql.UUID, primary_key=True, server_default=db.text('uuid_generate_v4()'))
    email = db.Column(db.Unicode, nullable=False, unique=True)
    password = db.Column(db.Unicode, nullable=False)
    name = db.Column(db.Unicode, nullable=False)

    def __repr__(self):
        """User repr."""
        return '<User email: {!} name: {!r}>'.format(self.email, self.name)


class Feed(db.Model):
    """Model that holds all feeds."""

    id = db.Column(postgresql.UUID, primary_key=True, server_default=db.text('uuid_generate_v4()'))
    name = db.Column(db.Unicode, nullable=True)
    url = db.Column(db.Unicode, nullable=False, unique=True)

    def __repr__(self):
        """Feed repr."""
        return '<Feed name: {!r} url: {!r}>'.format(self.name, self.url)


class Article(db.Model):
    """Article model. Represents the items in a feed."""

    id = db.Column(postgresql.UUID, primary_key=True, server_default=db.text('uuid_generate_v4()'))

    feed_id = db.Column(db.ForeignKey('feed.id'), nullable=False)
    feed = db.relationship(Feed)

    title = db.Column(db.Unicode, nullable=False)
    url = db.Column(db.Unicode, nullable=False)
    html_text = db.Column(db.Unicode, nullable=False)
    clean_text = db.Column(db.Unicode, nullable=False)
    publication_date = db.Column(postgresql.TIMESTAMP('UTC'), nullable=False)


class Subscription(db.Model):
    """Model that associates a user with a feed."""

    id = db.Column(postgresql.UUID, primary_key=True, server_default=db.text('uuid_generate_v4()'))

    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)

    feed_id = db.Column(db.ForeignKey('feed.id'), nullable=False)
    feed = db.relationship(Feed)


class Rating(db.Model):
    """Model used to save ratings and status of the `Article` of a `Subscription` of the user."""

    id = db.Column(postgresql.UUID, primary_key=True, server_default=db.text('uuid_generate_v4()'))

    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)

    article_id = db.Column(db.ForeignKey('article.id'), nullable=False)
    article = db.relationship(Article)

    # Cached column, can be determined from article_id; useful for filtering, grouping and sorting.
    feed_id = db.Column(db.ForeignKey('feed.id'), nullable=False)
    feed = db.relationship(Feed)

    # Both can be nullable, because they can be generated at different times
    user_rating = db.Column(db.DECIMAL(4, 2))
    machine_rating = db.Column(db.DECIMAL(4, 2))

    read = db.Column(db.Boolean(), nullable=False, default=False, server_default=db.text('FALSE'))
