"""24.12.16 - corrige precisao de valores decimais

Revision ID: b226a301d63f
Revises: a32d69048866
Create Date: 2024-12-16 14:27:16.473857

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'b226a301d63f'
down_revision = 'a32d69048866'
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
    session.execute(
        '''
        -- 17.4 -> 23.10
        ALTER TABLE cliente_estabelecimento
        ALTER COLUMN custo_por_quilo TYPE NUMERIC(23,10);
        ALTER TABLE cliente_estabelecimento
        ALTER COLUMN iluminacao_publica_media TYPE NUMERIC(23,10);
        ALTER TABLE cliente_estabelecimento
        ALTER COLUMN preco_referencia TYPE NUMERIC(23,10);
        ALTER TABLE cliente_estabelecimento
        ALTER COLUMN desconto_nominal TYPE NUMERIC(23,10);


        ALTER TABLE cliente_tarefa
        ALTER COLUMN custo_por_quilo TYPE NUMERIC(23,10);
        ALTER TABLE cliente_tarefa
        ALTER COLUMN iluminacao_publica_media TYPE NUMERIC(23,10);
        ALTER TABLE cliente_tarefa
        ALTER COLUMN preco_referencia TYPE NUMERIC(23,10);
        ALTER TABLE cliente_tarefa
        ALTER COLUMN desconto_nominal TYPE NUMERIC(23,10);


        -- 17.2 -> 23.10
        ALTER TABLE conta_energia
        ALTER COLUMN leitura_anterior TYPE NUMERIC(23,10);
        ALTER TABLE conta_energia
        ALTER COLUMN leitura_atual TYPE NUMERIC(23,10);
        ALTER TABLE conta_energia
        ALTER COLUMN diferenca_leituras TYPE NUMERIC(23,10);
        ALTER TABLE conta_energia
        ALTER COLUMN preco_referencia TYPE NUMERIC(23,10);
        ALTER TABLE conta_energia
        ALTER COLUMN iluminacao_publica_media TYPE NUMERIC(23,10);
        ALTER TABLE conta_energia
        ALTER COLUMN total_cosern TYPE NUMERIC(23,10);
        ALTER TABLE conta_energia
        ALTER COLUMN desconto_nominal_valor TYPE NUMERIC(23,10);
        ALTER TABLE conta_energia
        ALTER COLUMN desconto_nominal_porcentagem TYPE NUMERIC(23,10);
        ALTER TABLE conta_energia
        ALTER COLUMN desconto_efetivo_valor TYPE NUMERIC(23,10);
        ALTER TABLE conta_energia
        ALTER COLUMN desconto_efetivo_porcentagem TYPE NUMERIC(23,10);
        ALTER TABLE conta_energia
        ALTER COLUMN total_tarefa TYPE NUMERIC(23,10);
        ALTER TABLE conta_energia
        ALTER COLUMN cat TYPE NUMERIC(23,10);
        ALTER TABLE conta_energia
        ALTER COLUMN custo_por_quilo TYPE NUMERIC(23,10);
        '''
    )


def downgrade():
    pass
