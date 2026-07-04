"""create document_chunk table

Revision ID: a9a8f30f012a
Revises: abaa16e60e1a
Create Date: 2026-07-04 21:08:25.026724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import pgvector.sqlalchemy

# revision identifiers, used by Alembic.
revision: str = 'a9a8f30f012a'
down_revision: Union[str, Sequence[str], None] = 'abaa16e60e1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute("ALTER TYPE extractionstatus ADD VALUE IF NOT EXISTS 'INDEXED'")
    op.create_table('document_chunk',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('extraction_id', sa.Integer(), nullable=False),
    sa.Column('chunk_index', sa.Integer(), nullable=False),
    sa.Column('content', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('embedding', pgvector.sqlalchemy.vector.VECTOR(dim=1024), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['extraction_id'], ['extraction.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_document_chunk_embedding_hnsw', 'document_chunk', ['embedding'], unique=False, postgresql_using='hnsw', postgresql_ops={'embedding': 'vector_cosine_ops'})
    op.create_index(op.f('ix_document_chunk_extraction_id'), 'document_chunk', ['extraction_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_document_chunk_extraction_id'), table_name='document_chunk')
    op.drop_index('ix_document_chunk_embedding_hnsw', table_name='document_chunk', postgresql_using='hnsw', postgresql_ops={'embedding': 'vector_cosine_ops'})
    op.drop_table('document_chunk')
