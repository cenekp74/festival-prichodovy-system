"""empty message

Revision ID: acd9ab6e3f35
Revises: cd0731fec577
Create Date: 2024-06-02 10:54:38.411933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acd9ab6e3f35'
down_revision = 'cd0731fec577'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rfid', sa.String(length=10), nullable=True))
        batch_op.create_unique_constraint('rfid', ['rfid'])
        batch_op.drop_column('cip')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cip', sa.VARCHAR(length=10), nullable=True))
        batch_op.drop_constraint('rfid', type_='unique')
        batch_op.drop_column('rfid')

    # ### end Alembic commands ###
