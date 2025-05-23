"""Fix relationships

Revision ID: 0f1477562016
Revises: 159376722a5f
Create Date: 2025-03-27 12:21:36.299011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f1477562016'
down_revision: Union[str, None] = '159376722a5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('prescriptions', sa.Column('details', sa.String(), nullable=False))
    op.drop_constraint('prescriptions_patient_id_fkey', 'prescriptions', type_='foreignkey')
    op.drop_constraint('prescriptions_doctor_id_fkey', 'prescriptions', type_='foreignkey')
    op.drop_constraint('prescriptions_medicine_id_fkey', 'prescriptions', type_='foreignkey')
    op.create_foreign_key(None, 'prescriptions', 'patients', ['patient_id'], ['id'])
    op.drop_column('prescriptions', 'doctor_id')
    op.drop_column('prescriptions', 'dosage')
    op.drop_column('prescriptions', 'medicine_id')
    op.drop_column('prescriptions', 'instructions')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('prescriptions', sa.Column('instructions', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('prescriptions', sa.Column('medicine_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('prescriptions', sa.Column('dosage', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('prescriptions', sa.Column('doctor_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'prescriptions', type_='foreignkey')
    op.create_foreign_key('prescriptions_medicine_id_fkey', 'prescriptions', 'medicines', ['medicine_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('prescriptions_doctor_id_fkey', 'prescriptions', 'doctors', ['doctor_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('prescriptions_patient_id_fkey', 'prescriptions', 'patients', ['patient_id'], ['id'], ondelete='CASCADE')
    op.drop_column('prescriptions', 'details')
    # ### end Alembic commands ###
