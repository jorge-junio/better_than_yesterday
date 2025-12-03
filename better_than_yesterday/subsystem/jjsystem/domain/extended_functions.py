from jjsystem.common.operation_after_post import do_after_post
from better_than_yesterday.subsystem.jjsystem.domain.manager import (
    Manager as DomainManager,
    Register)
from better_than_yesterday.subsystem.jjsystem.domain import constants


@do_after_post(manager=DomainManager, operation=Register)
def on_register(operation):
    # seta as regras default ao cria um domínio
    regras_default = constants.REGRAS_DEFAULT
    operation.manager.update_settings(id=operation.domain.id, **regras_default)
