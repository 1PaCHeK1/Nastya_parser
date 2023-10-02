"""empty message

Revision ID: be7905623b59
Revises:
Create Date: 2023-01-09 20:11:05.573191

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "be7905623b59"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "languages",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("order", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(length=128), nullable=True),
        sa.Column("email", sa.String(length=128), nullable=True),
        sa.Column("tg_id", sa.Integer(), nullable=True),
        sa.Column("create_at", sa.Date(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("tg_id"),
    )
    op.create_table(
        "translates",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("from_language_id", sa.Integer(), nullable=True),
        sa.Column("to_language_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["from_language_id"],
            ["languages.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["to_language_id"],
            ["languages.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "words",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("text", sa.String(), nullable=True),
        sa.Column("language_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["language_id"], ["languages.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "favoriteword",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("word_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["word_id"], ["words.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "wordtranslates",
        sa.Column("word_from_id", sa.Integer(), nullable=False),
        sa.Column("word_to_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["word_from_id"], ["words.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["word_to_id"], ["words.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("word_from_id", "word_to_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("wordtranslates")
    op.drop_table("favoriteword")
    op.drop_table("words")
    op.drop_table("translates")
    op.drop_table("users")
    op.drop_table("languages")
    # ### end Alembic commands ###
