"""
add object_id to logs

Revision ID: 0004_add_object_id
Revises: 2ff824309330
Create Date: 2025-06-27 09:14:02.533685
"""
from typing import Union, Sequence

from alembic import op
import sqlalchemy as sa

# Alembic metadata
revision: str = "0004_add_object_id"
down_revision: Union[str, Sequence[str], None] = "2ff824309330"
branch_labels = None
depends_on = None


# upgrade -> добавляем колонку object_id (NOT NULL)
def upgrade() -> None:
    # batch_alter_table сохраняет существующие FK / индексы
    with op.batch_alter_table("logs", schema=None) as batch:
        batch.add_column(
            sa.Column(
                "object_id",
                sa.Integer(),
                nullable=False,
                server_default="0", # временно, чтобы обновить существующие строки
            )
        )

    # убираем default, чтобы колонка стала "обязательной"
    op.execute("ALTER TABLE logs ALTER COLUMN object_id DROP DEFAULT")


# downgrade -> откатываем изменение
def downgrade() -> None:
    with op.batch_alter_table("logs", schema=None) as batch:
        batch.drop_column("object_id")
