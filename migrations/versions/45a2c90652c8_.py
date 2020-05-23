"""empty message

Revision ID: 45a2c90652c8
Revises: ef446c1ed469
Create Date: 2020-05-23 19:49:16.652859

"""
from alembic import op
import sqlalchemy as sa

from utilities import *


# revision identifiers, used by Alembic.
revision = '45a2c90652c8'
down_revision = 'ef446c1ed469'
branch_labels = None
depends_on = None


def upgrade():
    convert_data_to_json()
    json_teachers_to_db()
    json_timeslots_to_db()
    json_goals_to_db()
    json_teachers_goals_to_db()


def downgrade():
    pass
