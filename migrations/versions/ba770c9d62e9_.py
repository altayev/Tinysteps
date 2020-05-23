"""empty message

Revision ID: ba770c9d62e9
Revises: 
Create Date: 2020-05-23 13:39:53.228734

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ba770c9d62e9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('students')
    op.drop_table('users')
    op.drop_table('bookings')
    op.drop_table('goals')
    op.drop_table('teacher_goals')
    op.drop_table('teachers')
    op.drop_table('timeslots')
    op.drop_table('requests')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('requests',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('have_time', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('goal', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], name='requests_student_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='requests_pkey')
    )
    op.create_table('timeslots',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('timeslots_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('teacher_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('weekday', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('time', postgresql.TIME(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='timeslots_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('teachers',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('about', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('rating', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('picture', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('price', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='teachers_pkey'),
    sa.UniqueConstraint('email', name='teachers_email_key')
    )
    op.create_table('teacher_goals',
    sa.Column('teacher_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('goal_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['goal_id'], ['goals.id'], name='teacher_goals_goal_id_fkey')
    )
    op.create_table('goals',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('goal_slug', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('goal_text', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='goals_pkey')
    )
    op.create_table('bookings',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('teacher_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('timeslot_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], name='bookings_student_id_fkey'),
    sa.ForeignKeyConstraint(['timeslot_id'], ['timeslots.id'], name='bookings_timeslot_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='bookings_pkey')
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key')
    )
    op.create_table('students',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='students_pkey')
    )
    # ### end Alembic commands ###
