
import flask

from datetime import datetime

from better_than_yesterday.subsystem.integracao import tasks

from jjsystem.common import exception
from jjsystem.common.subsystem import entity, operation, manager


class QueueSubroutine(operation.Create):

    def _valida_data(self, data):
        try:
            data = datetime.strptime(data, entity.DATE_FMT)
            return data
        except Exception:
            raise exception.BadRequest('A data de início não é válida!')

    def pre(self, **kwargs):
        self.ids = kwargs.get('ids', [])
        self.pacote = kwargs.get('pacote', None)
        self.data_inicio = kwargs.get('data_inicio', None)

        self.user_id = None
        if flask.has_request_context():
            token_id = flask.request.headers.get('token')
            if token_id is not None:
                self.token = self.manager.api.tokens().get(id=token_id)
                self.user_id = self.token.user_id

        if len(self.ids) == 0:
            raise exception.BadRequest('Não foi listado nenhum ID!')

        if self.pacote is None:
            raise exception.BadRequest('O pacote desejado não foi informado!')

        if self.data_inicio is not None:
            data = self._valida_data(self.data_inicio)
            self.data_inicio = str(data).replace(' ', 'T') + 'Z'

        return True

    def do(self, session, **kwargs):
        for domain_id in self.ids:
            domain = self.manager.api.domains().list(id=domain_id)
            if len(domain) == 0:
                pass

            payload = {
                'entity_name': self.pacote,
                'type': 'SYNC',
                'starting_date': self.data_inicio,
                'user_id': self.user_id
            }
            tasks.publish_queue_subroutine((domain_id, payload))

        return True


class Manager(manager.Manager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.queue_subroutine = QueueSubroutine(self)
