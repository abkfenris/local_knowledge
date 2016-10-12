"""Initial User, Way, and Node models

Revision ID: 3e82cddda66b
Revises: None
Create Date: 2016-10-11 19:56:32.171914

"""

# revision identifiers, used by Alembic.
revision = '3e82cddda66b'
down_revision = None

from alembic import op
import sqlalchemy as sa
import geoalchemy2
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('node',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('osm_id', sa.BigInteger(), nullable=True),
    sa.Column('geom', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326), nullable=True),
    sa.Column('json', postgresql.JSONB(astext_type=sa.types.Text()), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('way',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('osm_id', sa.BigInteger(), nullable=True),
    sa.Column('geom', geoalchemy2.types.Geometry(geometry_type='LINESTRING', srid=4326), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('json', postgresql.JSONB(astext_type=sa.types.Text()), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('way')
    op.drop_table('user')
    op.drop_table('node')
    ### end Alembic commands ###
