"""empty message

Revision ID: 34be3c14dac7
Revises: f1154564f2c4
Create Date: 2020-09-27 04:24:44.500119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34be3c14dac7'
down_revision = 'f1154564f2c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=255), nullable=True))
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_column('users', 'email')
    # ### end Alembic commands ###