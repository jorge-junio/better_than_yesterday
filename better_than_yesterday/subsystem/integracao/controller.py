
import flask

from jjsystem.common import exception
from jjsystem.common.subsystem import controller


class Controller(controller.Controller):

    def queue_subroutine(self):
        try:
            data = flask.request.get_json()
            self.manager.queue_subroutine(**data)
        except exception.JJSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(status=200,
                              mimetype="application/json")
