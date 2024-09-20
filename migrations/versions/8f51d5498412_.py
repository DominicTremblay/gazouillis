"""empty message

Revision ID: 8f51d5498412
Revises: 
Create Date: 2024-09-19 17:26:16.350879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f51d5498412'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('utilisateur',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(length=64), nullable=False),
    sa.Column('courriel', sa.String(length=120), nullable=False),
    sa.Column('mot_passe_hash', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('utilisateur', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_utilisateur_courriel'), ['courriel'], unique=True)
        batch_op.create_index(batch_op.f('ix_utilisateur_nom'), ['nom'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('utilisateur', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_utilisateur_nom'))
        batch_op.drop_index(batch_op.f('ix_utilisateur_courriel'))

    op.drop_table('utilisateur')
    # ### end Alembic commands ###
