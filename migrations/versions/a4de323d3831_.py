"""empty message

Revision ID: a4de323d3831
Revises: 15dc4e1121d8
Create Date: 2024-04-11 09:14:01.846345

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a4de323d3831'
down_revision = '15dc4e1121d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recetas', schema=None) as batch_op:
        batch_op.alter_column('nombre',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recetas', schema=None) as batch_op:
        batch_op.alter_column('nombre',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=True)

    # ### end Alembic commands ###