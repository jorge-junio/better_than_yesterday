from jjsystem.subsystem.token import manager


class Manager(manager.Manager):

    def __init__(self, driver):
        super().__init__(driver)

    def _normalize_datas(self, session):
        normalizar_municipio = '''
            UPDATE municipio m
            SET nome = (SELECT UPPER(jjsystem_normalize(m.nome))
                        FROM municipio m2
                        WHERE m.id = m2.id
                        LIMIT 1);
            '''
        session.execute(normalizar_municipio)
