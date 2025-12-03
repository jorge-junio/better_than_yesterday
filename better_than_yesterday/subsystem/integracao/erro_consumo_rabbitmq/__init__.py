from jjsystem.common import subsystem
from better_than_yesterday.subsystem.integracao.erro_consumo_rabbitmq import resource

subsystem = subsystem.Subsystem(resource=resource.ErroConsumoRabbitmq)
