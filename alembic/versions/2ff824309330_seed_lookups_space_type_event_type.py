from alembic import op
import sqlalchemy as sa

revision = "2ff824309330"
down_revision = "65413921dd36"
branch_labels = None
depends_on = None


def upgrade() -> None:
    space_type = sa.table(
        "space_type",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
    )
    event_type = sa.table(
        "event_type",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
    )

    op.bulk_insert(
        space_type,
        [
            {"id": 1, "name": "global"},
            {"id": 2, "name": "blog"},
            {"id": 3, "name": "post"},
        ],
    )
    op.bulk_insert(
        event_type,
        [
            {"id": 1, "name": "login"},
            {"id": 2, "name": "comment"},
            {"id": 3, "name": "create_post"},
            {"id": 4, "name": "delete_post"},
            {"id": 5, "name": "logout"},
        ],
    )


def downgrade() -> None:
    op.execute("TRUNCATE event_type, space_type CASCADE")
