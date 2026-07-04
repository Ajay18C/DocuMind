"""add page_number and nullable embedding to document_chunk

Revision ID: e931f1a8ecd7
Revises: a9a8f30f012a
Create Date: 2026-07-04 22:47:31.884920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector.sqlalchemy

# revision identifiers, used by Alembic.
revision: str = 'e931f1a8ecd7'
down_revision: Union[str, Sequence[str], None] = 'a9a8f30f012a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DELETE FROM document_chunk")
    op.add_column('document_chunk', sa.Column('page_number', sa.Integer(), nullable=False))
    op.alter_column('document_chunk', 'embedding',
               existing_type=pgvector.sqlalchemy.vector.VECTOR(dim=1024),
               nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM document_chunk WHERE embedding IS NULL")
    op.alter_column('document_chunk', 'embedding',
               existing_type=pgvector.sqlalchemy.vector.VECTOR(dim=1024),
               nullable=False)
    op.drop_column('document_chunk', 'page_number')
