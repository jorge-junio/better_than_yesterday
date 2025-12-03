from better_than_yesterday.subsystem.integracao import entity_consumer_handler
from better_than_yesterday.subsystem.integracao.consumers.consumer_parceiro import \
    ParceiroConsumerHandler


entity_consumer_handler('parceiro')(ParceiroConsumerHandler)
