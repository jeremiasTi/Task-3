"""create authors and books

Revision ID: 0001_create_authors_and_books
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_create_authors_and_books"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_authors_email"), "authors", ["email"], unique=False)
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("isbn", sa.String(length=20), nullable=False),
        sa.Column("published_year", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["author_id"], ["authors.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("isbn"),
    )
    op.create_index(op.f("ix_books_author_id"), "books", ["author_id"], unique=False)
    op.create_index(op.f("ix_books_isbn"), "books", ["isbn"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_books_isbn"), table_name="books")
    op.drop_index(op.f("ix_books_author_id"), table_name="books")
    op.drop_table("books")
    op.drop_index(op.f("ix_authors_email"), table_name="authors")
    op.drop_table("authors")

