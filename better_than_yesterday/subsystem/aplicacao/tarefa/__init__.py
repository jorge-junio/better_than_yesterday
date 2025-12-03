from better_than_yesterday.subsystem.aplicacao.tarefa \
    import extended_functions  # noqa: F401

from jjsystem.common import subsystem
from better_than_yesterday.subsystem.aplicacao.tarefa import resource, \
    controller, manager, router

subsystem = subsystem.Subsystem(resource=resource.Tarefa,
                                controller=controller.Controller,
                                manager=manager.Manager,
                                router=router.Router)
