
from better_than_yesterday.subsystem.jjsystem import (
    token, domain, constant_for_calculation)
from better_than_yesterday.subsystem.jjlocal import (
    ibge_sync)

from better_than_yesterday.subsystem import integracao
from better_than_yesterday.subsystem.aplicacao import (
    tarefa
)

packages = [
    constant_for_calculation.subsystem,
    domain.subsystem,
    tarefa.subsystem,
    ibge_sync.subsystem,
    integracao.subsystem,
    token.subsystem
]
