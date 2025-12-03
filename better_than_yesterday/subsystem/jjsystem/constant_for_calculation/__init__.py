from jjsystem.common import subsystem
from jjsystem.subsystem.constant_for_calculation \
    import resource, router, manager
from better_than_yesterday.subsystem.jjsystem.constant_for_calculation import controller

subsystem = subsystem.Subsystem(resource=resource.ConstantForCalculation,
                                router=router.Router,
                                controller=controller.Controller,
                                manager=manager.Manager)
