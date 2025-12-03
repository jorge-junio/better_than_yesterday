"""24.08.21 - add funcoes de domain sequence

Revision ID: 61cae89c60ff
Revises: 353827c93ebe
Create Date: 2024-08-21 23:17:26.348095

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '61cae89c60ff'
down_revision = '353827c93ebe'
branch_labels = None
depends_on = None


def create_session(op):
    from sqlalchemy.orm import sessionmaker

    _session = sessionmaker()
    bind = op.get_bind()
    session = _session(bind=bind)

    return session


def upgrade():
    sql_create_normalize = '''
        CREATE OR REPLACE FUNCTION jjsystem_normalize(text)
        RETURNS text
        IMMUTABLE
        STRICT
        LANGUAGE SQL
        AS $$
        SELECT trim(regexp_replace(translate(
            lower($1),
            'áàâãäåāăąèééêëēĕėęěìíîïìĩīĭḩóôõöōŏőùúûüũūŭůäàáâãåæçćĉčöòóôõøüùúûßéèêëýñîìíïşṕ',
            'aaaaaaaaaeeeeeeeeeeiiiiiiiihooooooouuuuuuuuaaaaaaeccccoooooouuuuseeeeyniiiisp'
        ), '[^a-z0-9%\-]+', ' ', 'g'));
        $$;
    '''  # noqa: W605
    sql_create_domain_and_table_seq_nextval = '''
        CREATE OR REPLACE FUNCTION domain_and_table_seq_nextval(p_domain_id CHAR(32), p_table_id CHAR(32), p_sequence_name VARCHAR(100), p_step NUMERIC(3) DEFAULT 1)
        RETURNS BIGINT
        LANGUAGE plpgsql
        AS $$ DECLARE
        l_domain_and_table_seq_value NUMERIC;
        BEGIN
        IF p_step <= 0 THEN
            RAISE EXCEPTION 'p_step param must be greater than zero.';
        END IF;

        UPDATE domain_and_table_sequence
        SET    value = value + COALESCE(p_step, 1, 1, p_step)
        WHERE  p_domain_id = domain_id AND
                p_table_id = table_id AND
                p_sequence_name = name
        RETURNING value INTO l_domain_and_table_seq_value;

        IF l_domain_and_table_seq_value IS NOT NULL THEN
            -- Se houve update o "value" e atualizado e retornado
            RETURN l_domain_and_table_seq_value;
        ELSE
            -- Se nao houve UPDATE nos registros, uma nova sequencia e criada
            -- com "value" e "step" igual p_step e retorna p_step.
            INSERT
            INTO   domain_and_table_sequence(id, domain_id, table_id, name, value)
            VALUES (REPLACE(CONCAT(uuid_generate_v4(), ''), '-', ''), p_domain_id, p_table_id, p_sequence_name, p_step);

            RETURN p_step;
        END IF;
        COMMIT;
        END;
        $$;
    '''  # noqa: E501
    sql_create_domain_seq_nextval = '''
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

        CREATE OR REPLACE FUNCTION domain_seq_nextval(p_domain_id CHAR(32), p_sequence_name VARCHAR(100), p_step NUMERIC(3) DEFAULT 1)
        RETURNS BIGINT
        LANGUAGE plpgsql
        AS $$ DECLARE
        l_domain_seq_value NUMERIC;
        BEGIN
        IF p_step <= 0 THEN
            RAISE EXCEPTION 'p_step param must be greater than zero.';
        END IF;

        UPDATE domain_sequence
        SET    value = value + COALESCE(p_step, 1, 1, p_step)
        WHERE  p_domain_id = domain_id AND
                p_sequence_name = name
        RETURNING value INTO l_domain_seq_value;

        IF l_domain_seq_value IS NOT NULL THEN
            -- Se houve update o "value" e atualizado e retornado
            RETURN l_domain_seq_value;
        ELSE
            -- Se nao houve UPDATE nos registros, uma nova sequencia e criada
            -- com "value" e "step" igual p_step e retorna p_step.
            INSERT
            INTO   domain_sequence(id, domain_id, name, value)
            VALUES (REPLACE(CONCAT(uuid_generate_v4(), ''), '-', ''), p_domain_id, p_sequence_name, p_step);

            RETURN p_step;
        END IF;
        COMMIT;
        END;
        $$;
    '''  # noqa: E501

    session = create_session(op)
    session.execute(sql_create_normalize)
    session.execute(sql_create_domain_seq_nextval)
    session.execute(sql_create_domain_and_table_seq_nextval)


def downgrade():
    sql_drop_normalize = '''DROP FUNCTION IF EXISTS viggocore_normalize;'''
    sql_drop_domain_and_table_seq_nextval = '''DROP FUNCTION IF EXISTS domain_and_table_seq_nextval;'''  # noqa
    sql_drop_domain_seq_nextval = '''DROP FUNCTION IF EXISTS domain_seq_nextval;'''  # noqa

    session = create_session(op)
    session.execute(sql_drop_normalize)
    session.execute(sql_drop_domain_seq_nextval)
    session.execute(sql_drop_domain_and_table_seq_nextval)
