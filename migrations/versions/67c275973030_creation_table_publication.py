"""creation_table_publication

Revision ID: 67c275973030
Revises: 8f51d5498412
Create Date: 2024-09-19 17:49:08.761403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67c275973030'
down_revision = '8f51d5498412'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('publication',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contenu', sa.String(length=140), nullable=False),
    sa.Column('horodatage', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['utilisateur.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('publication', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_publication_horodatage'), ['horodatage'], unique=False)
        batch_op.create_index(batch_op.f('ix_publication_user_id'), ['user_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('publication', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_publication_user_id'))
        batch_op.drop_index(batch_op.f('ix_publication_horodatage'))

    op.drop_table('publication')
    # ### end Alembic commands ###
