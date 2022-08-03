"""Added required tables

Revision ID: 768a9b58d2a7
Revises:
Create Date: 2022-07-28 21:55:14.121909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '768a9b58d2a7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('features',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('feature', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('room_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type_name', sa.String(), nullable=False),
    sa.Column('price', sa.Numeric(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_room_types_price'), 'room_types', ['price'], unique=False)
    op.create_table('rooms',
    sa.Column('number', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('fk_room_types_id', sa.Integer(), nullable=True),
    sa.Column('floor', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('housing', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.ForeignKeyConstraint(['fk_room_types_id'], ['room_types.id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('number')
    )
    op.create_table('roomtypes_features',
    sa.Column('fk_room_type_id', sa.Integer(), nullable=True),
    sa.Column('fk_feature_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['fk_feature_id'], ['features.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['fk_room_type_id'], ['room_types.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.UniqueConstraint('fk_room_type_id', 'fk_feature_id')
    )
    op.create_table('guests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fk_room_number', sa.Integer(), nullable=True),
    sa.Column('fk_guest_id', sa.Integer(), nullable=True),
    sa.Column('check_in', sa.DateTime(), nullable=False),
    sa.Column('check_out', sa.DateTime(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('is_paid', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('client_review', sa.String(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['fk_guest_id'], ['guests.id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['fk_room_number'], ['rooms.number'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bookings_check_in'), 'bookings', ['check_in'], unique=False)
    op.create_index(op.f('ix_bookings_check_out'), 'bookings', ['check_out'], unique=False)
    op.create_table('requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fk_booking_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('is_closed', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('close_description', sa.String(), nullable=True),
    sa.Column('price', sa.Numeric(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['fk_booking_id'], ['bookings.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fk_booking_id', sa.Integer(), nullable=True),
    sa.Column('sum', sa.Numeric(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['fk_booking_id'], ['bookings.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payments_date'), 'payments', ['date'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_payments_date'), table_name='payments')
    op.drop_table('payments')
    op.drop_table('requests')
    op.drop_index(op.f('ix_bookings_check_out'), table_name='bookings')
    op.drop_index(op.f('ix_bookings_check_in'), table_name='bookings')
    op.drop_table('bookings')
    op.drop_table('guests')
    op.drop_table('roomtypes_features')
    op.drop_table('rooms')
    op.drop_index(op.f('ix_room_types_price'), table_name='room_types')
    op.drop_table('room_types')
    op.drop_table('features')
    # ### end Alembic commands ###
