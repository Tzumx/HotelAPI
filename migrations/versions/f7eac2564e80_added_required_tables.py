"""Added required tables

Revision ID: f7eac2564e80
Revises: 
Create Date: 2022-07-26 15:50:23.396687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7eac2564e80'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('guests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('room_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=100), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('is_doublebad', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('is_kitchen', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('is_bathroom', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('is_conditioner', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('is_TV', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_room_types_price'), 'room_types', ['price'], unique=False)
    op.create_table('rooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('type_id', sa.Integer(), nullable=True),
    sa.Column('is_clean', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    sa.ForeignKeyConstraint(['type_id'], ['room_types.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rooms_number'), 'rooms', ['number'], unique=True)
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=True),
    sa.Column('guest_id', sa.Integer(), nullable=True),
    sa.Column('check_in', sa.DateTime(), nullable=False),
    sa.Column('check_out', sa.DateTime(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('is_paid', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('is_kitchen', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('is_check_in', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('is_check_out', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('is_need_food', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.Column('client_review', sa.String(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['guest_id'], ['guests.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bookings_check_in'), 'bookings', ['check_in'], unique=False)
    op.create_index(op.f('ix_bookings_check_out'), 'bookings', ['check_out'], unique=False)
    op.create_index(op.f('ix_bookings_total_price'), 'bookings', ['total_price'], unique=False)
    op.create_index(op.f('ix_bookings_updated_at'), 'bookings', ['updated_at'], unique=False)
    op.create_table('request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('booking_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('is_closed', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('close_desc', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['booking_id'], ['bookings.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_request_created_at'), 'request', ['created_at'], unique=False)
    op.create_index(op.f('ix_request_updated_at'), 'request', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_request_updated_at'), table_name='request')
    op.drop_index(op.f('ix_request_created_at'), table_name='request')
    op.drop_table('request')
    op.drop_index(op.f('ix_bookings_updated_at'), table_name='bookings')
    op.drop_index(op.f('ix_bookings_total_price'), table_name='bookings')
    op.drop_index(op.f('ix_bookings_check_out'), table_name='bookings')
    op.drop_index(op.f('ix_bookings_check_in'), table_name='bookings')
    op.drop_table('bookings')
    op.drop_index(op.f('ix_rooms_number'), table_name='rooms')
    op.drop_table('rooms')
    op.drop_index(op.f('ix_room_types_price'), table_name='room_types')
    op.drop_table('room_types')
    op.drop_table('guests')
    # ### end Alembic commands ###
