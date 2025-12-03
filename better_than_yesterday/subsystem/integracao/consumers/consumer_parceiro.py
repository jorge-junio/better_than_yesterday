from typing import Dict
from better_than_yesterday.subsystem.integracao.message import Message
from better_than_yesterday.subsystem.integracao.consumer import EntityConsumerHandler


class ParceiroConsumerHandler(EntityConsumerHandler):
    '''
    Consumer handler for Parceiro

    Handle events:

         - CREATED
         - UPDATED
    '''

    def handle(self, message: Message, api) -> bool:
        manager = api.parceiros()
        municipios_manager = api.municipios()
        enderecos = message.payload.get('enderecos', [])
        enderecos_mapped = map(
            lambda e: self.__map_endereco(e, municipios_manager),
            enderecos)
        message.payload['enderecos'] = list(enderecos_mapped)
        return self._handle_full_entity(message, manager)

    def __map_endereco(self, endereco: Dict, manager) -> Dict:
        codigo_ibge = endereco.pop('codigo_ibge', None)
        if codigo_ibge:
            municipios = manager.list(codigo_ibge=codigo_ibge)
            if municipios:
                endereco['municipio_id'] = municipios[0].id
        return endereco
