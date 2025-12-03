import flask
from jjsystem.common import utils
from jjsystem.subsystem.constant_for_calculation import controller
from better_than_yesterday.subsystem.jjsystem.constant_for_calculation.constant_table_names \
    import TABLE_NAMES


class Controller(controller.Controller):

    def __init__(self, manager, resource_wrap, collection_wrap):
        super(Controller, self).__init__(
            manager, resource_wrap, collection_wrap)

    def get_table_names(self):
        self.lista_table_names = TABLE_NAMES
        return super().get_table_names()
