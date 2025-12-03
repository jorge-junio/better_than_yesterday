from jjsystem.common.operation_after_post import do_after_post
from better_than_yesterday.subsystem.aplicacao.tarefa import constants, functions
from better_than_yesterday.subsystem.aplicacao.tarefa.manager import (
    Manager as ManagerTarefa,
    Create as CreateTarefa)


def _get_admin_user_id(operation):
    try:
        return operation.manager.api.users().list(
            domain_id=operation.entity.domain_id, name='admin')[0].id
    except Exception:
        return None


@do_after_post(manager=ManagerTarefa, operation=CreateTarefa)
def on_create(operation):

    # seta as regras default ao cria um domínio
    regras_default = constants.REGRAS_DEFAULT
    operation.manager.update_settings(id=operation.entity.id, **regras_default)

    # cria processo PCP
    admin_id = _get_admin_user_id(operation=operation)
    functions.criar_portador_padrao(
        operation=operation, created_by=admin_id)
    functions.criar_centro_resultado_padrao(
        operation=operation, created_by=admin_id)
    functions.criar_forma_pagto_dinheiro(
        operation=operation, created_by=admin_id)
    functions.criar_forma_pagto_pix(
        operation=operation, created_by=admin_id)
