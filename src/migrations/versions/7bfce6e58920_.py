"""empty message

Revision ID: 7bfce6e58920
Revises: cfad73abf1d6
Create Date: 2023-04-10 19:45:41.452417

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "7bfce6e58920"
down_revision = "cfad73abf1d6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "favoriteword",
        "user_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.alter_column(
        "favoriteword",
        "word_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.alter_column("languages", "name", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("languages", "order", existing_type=sa.INTEGER(), nullable=False)
    op.alter_column("post", "title", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("post", "body", existing_type=sa.TEXT(), nullable=False)
    op.alter_column("post", "author_id", existing_type=sa.INTEGER(), nullable=False)
    op.alter_column("post", "is_publish", existing_type=sa.BOOLEAN(), nullable=False)
    op.alter_column(
        "post",
        "publish_date",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
    )
    op.alter_column(
        "quizquestions",
        "question",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )
    op.alter_column(
        "quizquestions",
        "theme_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.alter_column(
        "quizquestions",
        "answer_one",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )
    op.alter_column(
        "quizquestions",
        "answer_two",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )
    op.alter_column(
        "quizquestions",
        "answer_three",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )
    op.alter_column(
        "quizquestions",
        "right_answer",
        existing_type=sa.VARCHAR(length=12),
        nullable=False,
    )
    op.alter_column("quiztheme", "name", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("tag", "name", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("tag", "rating", existing_type=sa.INTEGER(), nullable=False)
    op.alter_column(
        "translates",
        "from_language_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.alter_column(
        "translates",
        "to_language_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.alter_column("users", "create_at", existing_type=sa.DATE(), nullable=False)
    op.alter_column("users", "is_active", existing_type=sa.BOOLEAN(), nullable=False)
    op.alter_column("words", "text", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("words", "language_id", existing_type=sa.INTEGER(), nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("words", "language_id", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column("words", "text", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("users", "is_active", existing_type=sa.BOOLEAN(), nullable=True)
    op.alter_column("users", "create_at", existing_type=sa.DATE(), nullable=True)
    op.alter_column(
        "translates",
        "to_language_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.alter_column(
        "translates",
        "from_language_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.alter_column("tag", "rating", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column("tag", "name", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("quiztheme", "name", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column(
        "quizquestions",
        "right_answer",
        existing_type=sa.VARCHAR(length=12),
        nullable=True,
    )
    op.alter_column(
        "quizquestions",
        "answer_three",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.alter_column(
        "quizquestions",
        "answer_two",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.alter_column(
        "quizquestions",
        "answer_one",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.alter_column(
        "quizquestions",
        "theme_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.alter_column(
        "quizquestions",
        "question",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.alter_column(
        "post",
        "publish_date",
        existing_type=postgresql.TIMESTAMP(),
        nullable=True,
    )
    op.alter_column("post", "is_publish", existing_type=sa.BOOLEAN(), nullable=True)
    op.alter_column("post", "author_id", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column("post", "body", existing_type=sa.TEXT(), nullable=True)
    op.alter_column("post", "title", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("languages", "order", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column("languages", "name", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column(
        "favoriteword",
        "word_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.alter_column(
        "favoriteword",
        "user_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    # ### end Alembic commands ###
