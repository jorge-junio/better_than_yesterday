from better_than_yesterday.subsystem.jjsystem.domain \
    import extended_functions  # noqa: F401

from jjsystem.common import subsystem

from jjsystem.subsystem.domain import resource, controller, router
from better_than_yesterday.subsystem.jjsystem.domain import manager


subsystem = subsystem.Subsystem(resource=resource.Domain,
                                manager=manager.Manager,
                                router=router.Router,
                                controller=controller.Controller)
