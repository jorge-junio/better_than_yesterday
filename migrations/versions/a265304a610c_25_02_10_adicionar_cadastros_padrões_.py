"""25.02.10 - Adicionar cadastros padrões para cada Tarefa

Revision ID: a265304a610c
Revises: 8bf51961ef8b
Create Date: 2025-02-10 21:09:57.108706

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'a265304a610c'
down_revision = '8bf51961ef8b'
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
        """
        -- cadastra portador default CONTA CAIXA
        INSERT INTO public.portador
        (id, active, created_at, created_by, domain_id, tarefa_id, tipo, descricao, padrao, saldo, saldo_inicial)
        SELECT md5((random())::text), true, now(), f.user_id, f.domain_id, f.id, 'INTERNO', 'CONTA CAIXA', true, 0, 0
            FROM tarefa f
            JOIN "domain" d ON d.id = f.domain_id
            WHERE d."name" <> 'default' AND f.id NOT IN (SELECT tarefa_id FROM portador WHERE descricao = 'CONTA CAIXA');

        -- cadastro o centro de resultado default SETOR ADMINISTRATIVO
        INSERT INTO public.centro_resultado
        (id, active, created_at, created_by, domain_id, tarefa_id, descricao)
        SELECT md5((random())::text), true, now(), f.user_id, f.domain_id, f.id, 'SETOR ADMINISTRATIVO'
            FROM tarefa f
            JOIN "domain" d ON d.id = f.domain_id
            WHERE d."name" <> 'default' AND f.id NOT IN (SELECT tarefa_id FROM centro_resultado WHERE descricao = 'SETOR ADMINISTRATIVO');

        -- cadastra forma de pagamento default DINHEIRO
        INSERT INTO public.forma_pagamento
        (id, active, created_at, created_by, domain_id, tarefa_id, codigo, nome, a_prazo)
        SELECT md5((random())::text), true, now(), f.user_id, f.domain_id, f.id, 0, 'DINHEIRO', false
            FROM tarefa f
            JOIN "domain" d ON d.id = f.domain_id
            WHERE d."name" <> 'default' AND f.id NOT IN (SELECT tarefa_id FROM forma_pagamento WHERE codigo = 0 AND nome = 'DINHEIRO');

        -- cadastra forma de pagamento default PIX
        INSERT INTO public.forma_pagamento
        (id, active, created_at, created_by, domain_id, tarefa_id, codigo, nome, a_prazo)
        SELECT md5((random())::text), true, now(), f.user_id, f.domain_id, f.id, -1, 'PIX', false
            FROM tarefa f
            JOIN "domain" d ON d.id = f.domain_id
            WHERE d."name" <> 'default' AND f.id NOT IN (SELECT tarefa_id FROM forma_pagamento WHERE codigo = -1 AND nome = 'PIX');
        """)  # noqa


def downgrade():
    pass
