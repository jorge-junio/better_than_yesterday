
from jjsystem.common import subsystem
from jjsystem.subsystem.token import resource, router, controller

from better_than_yesterday.subsystem.jjsystem.token import manager

subsystem = subsystem.Subsystem(resource=resource.Token,
                                manager=manager.Manager,
                                router=router.Router,
                                controller=controller.Controller)
