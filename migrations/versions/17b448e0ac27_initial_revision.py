"""Initial revision.

Revision ID: 17b448e0ac27
Revises:
Create Date: 2016-08-17 13:26:43.288721
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "17b448e0ac27"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade instructions."""
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.create_table(
        "feed",
        sa.Column("id", postgresql.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("name", sa.Unicode(), nullable=True),
        sa.Column("url", sa.Unicode(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_feed")),
        sa.UniqueConstraint("url", name=op.f("uq_feed_url")),
    )
    op.create_table(
        "user",
        sa.Column("id", postgresql.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("email", sa.Unicode(), nullable=False),
        sa.Column("password", sa.Unicode(), nullable=False),
        sa.Column("name", sa.Unicode(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user")),
        sa.UniqueConstraint("email", name=op.f("uq_user_email")),
    )
    op.create_table(
        "article",
        sa.Column("id", postgresql.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("feed_id", postgresql.UUID(), nullable=False),
        sa.Column("title", sa.Unicode(), nullable=False),
        sa.Column("url", sa.Unicode(), nullable=False),
        sa.Column("html_text", sa.Unicode(), nullable=False),
        sa.Column("clean_text", sa.Unicode(), nullable=False),
        sa.Column("publication_date", postgresql.TIMESTAMP(timezone="UTC"), nullable=False),
        sa.ForeignKeyConstraint(["feed_id"], ["feed.id"], name=op.f("fk_article_feed_id_feed")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_article")),
    )
    op.create_table(
        "subscription",
        sa.Column("id", postgresql.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("user_id", postgresql.UUID(), nullable=False),
        sa.Column("feed_id", postgresql.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["feed_id"], ["feed.id"], name=op.f("fk_subscription_feed_id_feed")),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], name=op.f("fk_subscription_user_id_user")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_subscription")),
    )
    op.create_table(
        "rating",
        sa.Column("id", postgresql.UUID(), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("user_id", postgresql.UUID(), nullable=False),
        sa.Column("article_id", postgresql.UUID(), nullable=False),
        sa.Column("feed_id", postgresql.UUID(), nullable=False),
        sa.Column("user_rating", sa.DECIMAL(precision=4, scale=2), nullable=True),
        sa.Column("machine_rating", sa.DECIMAL(precision=4, scale=2), nullable=True),
        sa.Column("read", sa.Boolean(), server_default=sa.text("FALSE"), nullable=False),
        sa.ForeignKeyConstraint(["article_id"], ["article.id"], name=op.f("fk_rating_article_id_article")),
        sa.ForeignKeyConstraint(["feed_id"], ["feed.id"], name=op.f("fk_rating_feed_id_feed")),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], name=op.f("fk_rating_user_id_user")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_rating")),
    )


def downgrade():
    """Downgrade instructions."""
    op.drop_table("rating")
    op.drop_table("subscription")
    op.drop_table("article")
    op.drop_table("user")
    op.drop_table("feed")
