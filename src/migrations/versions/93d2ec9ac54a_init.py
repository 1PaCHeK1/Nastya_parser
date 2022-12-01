"""init

Revision ID: 93d2ec9ac54a
Revises: 
Create Date: 2022-11-24 19:05:57.457311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93d2ec9ac54a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('languages',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('tg_id', sa.Integer(), nullable=True),
    sa.Column('create_at', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('tg_id')
    )
    op.create_table('words',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('translate', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('translates',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('from_language_id', sa.Integer(), nullable=True),
    sa.Column('to_language_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['from_language_id'], ['languages.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['to_language_id'], ['languages.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favoriteword',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('word_id', sa.Integer(), nullable=True),
    sa.Column('translate_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['translate_id'], ['translates.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['word_id'], ['words.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favoriteword')
    op.drop_table('translates')
    op.drop_table('words')
    op.drop_table('users')
    op.drop_table('languages')
    # ### end Alembic commands ###