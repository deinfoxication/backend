"""Change feed and article to adapt the update task.

Revision ID: 4213edb3ce5a
Revises: 17b448e0ac27
Create Date: 2016-09-03 18:44:37.218086

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4213edb3ce5a"
down_revision = "17b448e0ac27"
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade instructions."""
    op.add_column("feed", sa.Column("last_etag", sa.Unicode(), nullable=True))


def downgrade():
    """Downgrade instructions."""
    op.drop_column("feed", "last_etag")
