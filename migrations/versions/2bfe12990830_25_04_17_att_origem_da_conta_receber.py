"""25.04.17 - Att coluna origem da conta_receber para tamanho 50

Revision ID: 2bfe12990830
Revises: 37fe72ceb1b4
Create Date: 2025-04-17 18:37:31.124107

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '2bfe12990830'
down_revision = '37fe72ceb1b4'
branch_labels = None
depends_on = None


def create_session(op):
    from sqlalchemy.orm import sessionmaker

    _session = sessionmaker()
    bind = op.get_bind()
    session = _session(bind=bind)

    return session


def upgrade():
    session = create_session(op)
    session.execute("""
        ALTER TABLE conta_receber
        ALTER COLUMN origem TYPE VARCHAR(50);""")


def downgrade():
    session = create_session(op)
    session.execute("""
        ALTER TABLE conta_receber
        ALTER COLUMN origem TYPE VARCHAR(5);""")
