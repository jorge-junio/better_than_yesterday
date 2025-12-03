
from better_than_yesterday.subsystem.integracao import controller, manager, resource, router

from jjsystem.common import exception, subsystem


subsystem = subsystem.Subsystem(individual_name='integracao',
                                collection_name='integracoes',
                                resource=resource.Integracao,
                                manager=manager.Manager,
                                controller=controller.Controller,
                                router=router.Router)


entity_consumer_handler_registry = dict()


def entity_consumer_handler(name: str):
    '''
    Decorator for register handlers for entities based on type

    Parameters:
        name (str): The key of entity handler.

    Returns:
        entity_consumer_handler(name)(cls): The original cls
    '''

    def wrapper(cls):
        if entity_consumer_handler_registry.get(name) is not None:
            raise exception.JJSystemException(
                f'The entity consumer handler {name} was already registered')

        entity_consumer_handler_registry[name] = cls
        return cls

    return wrapper
