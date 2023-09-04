"""empty message

Revision ID: 37c4de6b0df7
Revises: be7905623b59
Create Date: 2023-03-02 18:58:56.343400

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "37c4de6b0df7"
down_revision = "be7905623b59"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "quiztheme",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tag",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("rating", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "post",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("body", sa.Text(), nullable=True),
        sa.Column("author_id", sa.Integer(), nullable=True),
        sa.Column("is_publish", sa.Boolean(), nullable=True),
        sa.Column("publish_date", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "quizquestions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("question", sa.String(), nullable=True),
        sa.Column("theme_id", sa.Integer(), nullable=True),
        sa.Column("answer_one", sa.String(), nullable=True),
        sa.Column("answer_two", sa.String(), nullable=True),
        sa.Column("answer_three", sa.String(), nullable=True),
        sa.Column(
            "right_answer",
            sa.Enum(
                "answer_one",
                "answer_two",
                "answer_three",
                name="rightanswerenum",
                native_enum=False,
            ),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["theme_id"], ["quiztheme.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "posttags",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=True),
        sa.Column("post_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["post_id"], ["post.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tag_id"], ["tag.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("posttags")
    op.drop_table("quizquestions")
    op.drop_table("post")
    op.drop_table("tag")
    op.drop_table("quiztheme")
    # ### end Alembic commands ###
