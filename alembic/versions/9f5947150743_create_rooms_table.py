"""create rooms table

Revision ID: 9f5947150743
Revises:
Create Date: 2024-06-30 17:05:01.338994

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
import json


# revision identifiers, used by Alembic.
revision: str = '9f5947150743'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def remove_duplicates(data):
    seen_ids = set()
    unique_data = []
    for entry in data:
        if entry['id'] not in seen_ids:
            unique_data.append(entry)
            seen_ids.add(entry['id'])
    return unique_data


def upgrade() -> None:
    op.create_table(
        'rooms',
        sa.Column('name', sa.Text, nullable=True),
        sa.Column('id', sa.BigInteger, primary_key=True),
        schema='public'
    )
    op.execute('ALTER TABLE public.rooms OWNER TO postgres')
    rooms_table = table(
        'rooms',
        sa.Column('name', sa.Text),
        sa.Column('id', sa.BigInteger)
    )
    with open('rooms.json') as file:
        data = json.load(file)
        unique_data = remove_duplicates(data)
        op.bulk_insert(rooms_table, unique_data)


def downgrade() -> None:
    op.drop_table('rooms', schema='public')