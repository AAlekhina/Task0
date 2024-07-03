"""create students table

Revision ID: 5e42031cf23f
Revises:
Create Date: 2024-06-29 17:05:01.338994

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
import json

# revision identifiers, used by Alembic.
revision: str = '5e42031cf23f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Убедимся, что таблица существует перед попыткой удаления
    op.drop_table('students', schema='public', if_exists=True)

    op.create_table(
        'students',
        sa.Column('birthday', sa.Text, nullable=True),
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('name', sa.Text, nullable=True),
        sa.Column('room', sa.BigInteger, nullable=True),
        sa.Column('sex', sa.Text, nullable=True),
        schema='public'
    )
    op.execute('ALTER TABLE public.students OWNER TO postgres')

    students_table = table(
        'students',
        sa.Column('birthday', sa.Text),
        sa.Column('id', sa.BigInteger),
        sa.Column('name', sa.Text),
        sa.Column('room', sa.BigInteger),
        sa.Column('sex', sa.Text)
    )
    with open('students.json') as file:
        data = json.load(file)
        op.bulk_insert(students_table, data)


def downgrade() -> None:
    op.drop_table('students', schema='public', if_exists=True)