from jjsystem.subsystem.domain import manager
# imports adicionados para fazer o do_after_post funcionar corretamente
from jjsystem.subsystem.domain.manager import (  # noqa
    Register)


class GetUsageInfoByDomain(manager.GetUsageInfoByDomain):

    # vai pegar os totais de linhas em cada tabela do banco por domínio
    def _get_totals_by_domain(self, session):
        from better_than_yesterday.subsystem.jjsystem.domain.sql.totals_by_domain import QUERY
        rs = session.execute(QUERY.format(de=self.de, ate=self.ate))
        response = [r for r in rs]
        response_dict = [
            {
                'table_name': r[0],
                'total': self._get_value_or_default(value=r[1], tipo=int),
                'domain_name': r[2],
                'application_id': r[3],
                'application_name': r[4],
                'domain_id': r[5],
                'active': r[6]
            }
            for r in response]

        return response_dict

    # vai pegar os totais de linhas em cada tabela do banco
    def _get_totals_db(self, session):
        from better_than_yesterday.subsystem.jjsystem.domain.sql.totals_db import QUERY
        rs = session.execute(QUERY.format(de=self.de, ate=self.ate))
        response = [r for r in rs]
        response_dict = {
            r[0]: r[1]
            for r in response}

        return response_dict

    def do(self, session, **kwargs):
        return super().do(session, **kwargs)


class Manager(manager.Manager):

    def __init__(self, driver):
        super().__init__(driver)
        self.get_usage_info_by_domain = GetUsageInfoByDomain(self)
