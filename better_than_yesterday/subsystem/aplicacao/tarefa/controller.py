import flask
from jjsystem.common import exception, utils
from jjsystem.common.subsystem import controller


class Controller(controller.Controller):

    def create(self):
        data = flask.request.get_json()

        try:
            if data:
                entity = self.manager.create(**data)
            else:
                entity = self.manager.create()
        except exception.JJSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        tarefa_dict = entity.to_dict({'user': {}})
        response = {self.resource_wrap: tarefa_dict}

        return flask.Response(response=utils.to_json(response),
                              status=201,
                              mimetype=controller.DEFAULT_MIMETYPE)

    def update(self, id):
        data = flask.request.get_json()

        try:
            data.pop('id', None)
            entity = self.manager.update(id=id, **data)
        except exception.JJSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        tarefa_dict = entity.to_dict({'user': {}})
        response = {self.resource_wrap: tarefa_dict}

        return flask.Response(response=utils.to_json(response),
                              status=200,
                              mimetype=controller.DEFAULT_MIMETYPE)

    def list(self):
        return super().list()

    # início das funções das settings
    def update_settings(self, id):
        try:
            data = flask.request.get_json()

            settings = self.manager.update_settings(id=id, **data)
            response = {'settings': settings}

            return flask.Response(response=utils.to_json(response),
                                  status=200,
                                  mimetype="application/json")
        except exception.JJSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

    def _get_keys_from_args(self):
        keys = flask.request.args.get('keys')
        if not keys:
            raise exception.BadRequest(
                'ERRO! As chaves dos parâmetros não foram ' +
                'passados corretamente.')
        return list(filter(None, keys.split(',')))

    def remove_settings(self, id):
        try:
            keys = self._get_keys_from_args()
            kwargs = {'keys': keys}

            settings = self.manager.remove_settings(id=id, **kwargs)
            response = {'settings': settings}

            return flask.Response(response=utils.to_json(response),
                                  status=200,
                                  mimetype="application/json")
        except exception.JJSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

    def get_settings_by_keys(self, id):
        try:
            keys = self._get_keys_from_args()
            kwargs = {'keys': keys}

            settings = self.manager.get_settings_by_keys(
                id=id, **kwargs)
            response = {'id': id, 'settings': settings}

            return flask.Response(response=utils.to_json(response),
                                  status=200,
                                  mimetype="application/json")
        except exception.JJSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)
    # final das funções das settings
