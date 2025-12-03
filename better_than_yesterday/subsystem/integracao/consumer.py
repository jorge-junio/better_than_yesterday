from abc import ABC, abstractmethod
import json

from celery import bootsteps
from celery.utils.log import get_logger
from flask.globals import current_app
from kombu import Consumer, Exchange, Queue

from jjsystem.common.subsystem.manager import Manager
from jjsystem.queue import BasicQueueConsumer

from better_than_yesterday.subsystem.integracao import entity_consumer_handler_registry
from better_than_yesterday.subsystem.integracao.message import Message
from pika.exceptions import StreamLostError, ChannelWrongStateError


logger = get_logger(__name__)
consumer_queue = Queue('better_than_yesterday_from_integration',
                       Exchange('better_than_yesterday_from_integration', type='topic'),
                       '#')


class EntityConsumerHandler(ABC):

    @abstractmethod
    def handle(self, message: Message, api) -> bool:
        pass

    def _handle_full_entity(self, message: Message, manager: Manager) -> bool:
        operation = 'UPDATED' if manager.count(id=message.payload['id']) \
            else 'CREATED'

        mapper = {
            'CREATED': manager.create,
            'UPDATED': manager.update
        }
        action = mapper.get(operation)

        if action is not None:
            action(**message.payload)
        else:
            print(f'No event_type handle for {message.event_type}')

        return True


class RabbitmqConsumer(bootsteps.ConsumerStep):

    def get_consumers(self, channel):
        return [Consumer(channel,
                         queues=[consumer_queue],
                         callbacks=[self.handle_message],
                         accept=['json'],
                         no_ack=False,
                         prefetch_count=16)]

    def handle_message(self, body, message):
        try:
            parsed_message = self._parse_message(body, message)
            cls_handler = entity_consumer_handler_registry.\
                get(parsed_message.type)

            if cls_handler is None:
                log_message = f'''No entity consumer handler for type
                    {parsed_message.type} found'''
                logger.warn(log_message)
                message.ack()
                return

            handler = cls_handler()
            api = current_app.api_handler.api()
            is_success = handler.handle(parsed_message, api)

            if is_success:
                logger.info(f'{parsed_message} success')

            message.ack()
        except Exception as e:
            logger.error(str(e))
            message.ack()

    def _parse_message(self, body, message) -> Message:
        entity_type = message.properties.get('type')
        headers = message.properties.get('application_headers')
        event_type = headers.get('event_type') if headers else None
        routing_key = message.delivery_info.get('routing_key')
        return Message(entity_type, event_type, routing_key, body)


class BetterThanYesterdayFromIntegrationConsumer(BasicQueueConsumer):

    max_count_errors = 2
    exchanges = [
        {
            'exchange': 'better_than_yesterday_from_integration',
            'routing_key': '#',
            'type': 'topic'
        }
    ]

    queue_name = 'better_than_yesterday_from_integration'
    arguments = {
        'x-max-priority': 10,
        'x-dead-letter-routing-key': 'better_than_yesterday_from_integration_dl',
        'x-dead-letter-exchange': ''
    }

    def __init__(self, *args, **kwargs):
        super().__init__(self.queue_name, exchanges=self.exchanges,
                         prefetch_size=16, arguments=self.arguments,
                         *args, **kwargs)

    def run(self):
        self.declare_and_consume(self.handle_message)

    def __parse_message(self, body, method, properties) -> Message:
        entity_type = properties.type
        event_type = properties.headers.get('event_type', None)
        routing_key = method.routing_key
        body_dict = json.loads(body)
        return Message(entity_type, event_type, routing_key, body_dict)

    def handle_message(self, ch, method, properties, body):
        try:
            parsed_message = self.__parse_message(body, method, properties)
            cls_handler = entity_consumer_handler_registry.\
                get(parsed_message.type)

            if cls_handler is None:
                log_message = f'''No entity consumer handler for type
                    {parsed_message.type} found'''
                print('WARNING: ' + log_message)
                return

            handler = cls_handler()
            api = current_app.api_handler.api()
            is_sucess = handler.handle(parsed_message, api)

            if is_sucess:
                print(f'INFO: {parsed_message} success')

            ch.basic_ack(method.delivery_tag)
        except StreamLostError as e:
            raise e
        except ChannelWrongStateError as e:
            raise e
        except Exception as e:
            if (self.count_rejects_this_message(properties) >=
               self.max_count_errors):
                api = current_app.api_handler.api()
                erro_consumo_rabbitmq_dict = {
                    'message_type': properties.type,
                    'error': str(e),
                    'properties': str(properties),
                    'payload': str(body).replace("\'", "")[1:]
                }
                api.erro_consumo_rabbitmqs().create(
                    **erro_consumo_rabbitmq_dict)
                print('ERROR: ' + str(e))
                ch.basic_ack(method.delivery_tag)
            else:
                print('ERROR: ' + str(e))
                ch.basic_reject(method.delivery_tag, requeue=False)


class BetterThanYesterdayFromIntegrationDLConsumer(BasicQueueConsumer):

    exchanges = []

    queue_name = 'better_than_yesterday_from_integration_dl'
    arguments = {
        'x-dead-letter-routing-key': 'better_than_yesterday_from_integration',
        'x-dead-letter-exchange': ''
    }

    def __init__(self, *args, **kwargs):
        super().__init__(self.queue_name, exchanges=self.exchanges,
                         prefetch_size=16, arguments=self.arguments,
                         *args, **kwargs)

    def run(self):
        self.declare_and_consume(self.handle_message)

    def handle_message(self, ch, method, properties, body):
        try:
            ch.basic_reject(method.delivery_tag, requeue=False)
        except StreamLostError as e:
            raise e
        except ChannelWrongStateError as e:
            raise e
        except Exception as e:
            print('ERROR: ' + str(e))
            ch.basic_reject(method.delivery_tag, requeue=False)


class BetterThanYesterdayFromNuvemFiscalConsumer(BasicQueueConsumer):

    exchanges = [
        {
            'exchange': 'nuvem_fiscal_to_reprocess',
            'routing_key': '#',
            'type': 'topic'
        }
    ]

    queue_name = 'nuvem_fiscal_to_reprocess'
    arguments = {
        'x-max-priority': 10,
        'x-dead-letter-routing-key': 'nuvem_fiscal_to_reprocess_dl',
        'x-dead-letter-exchange': ''
    }

    msg_sucesso = 'SUCESSO: Mensagem consumida com sucesso!'
    msg_erro = 'ERRO: Ocorreu um erro no consumo da mensagem!'

    def __init__(self, *args, **kwargs):
        super().__init__(self.queue_name, exchanges=self.exchanges,
                         prefetch_size=16, arguments=self.arguments,
                         *args, **kwargs)

    def run(self):
        self.declare_and_consume(self.handle_message)

    def __parse_message(self, body, method, properties) -> Message:
        entity_type = properties.type
        event_type = properties.headers.get('event_type', None)
        routing_key = method.routing_key
        body_dict = json.loads(body)
        return Message(entity_type, event_type, routing_key, body_dict)

    def handle_message(self, ch, method, properties, body):
        pass
        # try:
        #     parsed_message = self.__parse_message(body, method, properties)
        #     if parsed_message.type == 'nfe':
        #         api = current_app.api_handler.api()
        #         api_fiscal = parsed_message.payload.get('api_fiscal', None)
        #         api_fiscal = cnf_tipo[api_fiscal]
        #         nota_id = parsed_message.payload.get('nota_id', '')
        #         nfe_id = parsed_message.payload.get('nfe_id', '')
        #         created_by = parsed_message.payload.get('created_by', '')
        #         response = api.nuvem_fiscals().consultar_nfe(
        #             **{'nfe_id': nota_id, 'api_fiscal': api_fiscal})
        #         response_dict = api.nuvem_fiscals().montar_response_dict(
        #             response)
        #         chave = response_dict.get('chave', None)
        #         autorizacao = response_dict.get('autorizacao', {})
        #         evento_status = response_dict.get('status', '')
        #         status_codigo = autorizacao.get('codigo_status', None)
        #         status_motivo = autorizacao.get('motivo_status', None)
        #         evento_dict = {
        #             'status': evento_status.upper(),
        #             'status_dh': autorizacao.get('data_evento', ''),
        #             'status_por': created_by,
        #             'evento_id': autorizacao.get('id', None),
        #             'status_codigo': status_codigo,
        #             'status_motivo': status_motivo,
        #             'nota_id': nota_id
        #         }
        #         if (evento_status in ['autorizado', 'denegado', 'encerrado',
        #                               'cancelado', 'erro']):
        #             api.nfes().reg_evento(id=nfe_id, **evento_dict)
        #             api.nfes().update_sem_remover_embedded(
        #                 id=nfe_id, **{'chave': chave})
        #             response = api.nuvem_fiscals().baixar_xml_nfe(
        #                 **{'nfe_id': nota_id, 'api_fiscal': api_fiscal})
        #             if response.status_code == 200:
        #                 response_dict = api.nuvem_fiscals().\
        #                     montar_response_dict(response)
        #                 api.nfes().update_sem_remover_embedded(
        #                     id=nfe_id,
        #                     **{'xml': response_dict.get('error', '')})
        #             print(self.msg_sucesso)
        #             ch.basic_ack(method.delivery_tag)
        #         elif evento_status in ['rejeitado']:
        #             inconsistencia = Inconsistencia(
        #                 status_codigo, status_motivo, 'SEFAZ')
        #             inconsistencias = [inconsistencia.to_dict()]
        #             api.nfes().reg_evento(id=nfe_id, **evento_dict)
        #             api.nfes().update_sem_remover_embedded(
        #                 id=nfe_id,
        #                 **{'chave': chave, 'inconsistencias': inconsistencias})
        #             response = api.nuvem_fiscals().baixar_xml_nota_nfe(
        #                 **{'nfe_id': nota_id, 'api_fiscal': api_fiscal})
        #             if response.status_code == 200:
        #                 response_dict = api.nuvem_fiscals().\
        #                     montar_response_dict(response)
        #                 api.nfes().update_sem_remover_embedded(
        #                     id=nfe_id,
        #                     **{'xml': response_dict.get('error', '')})
        #             print(self.msg_sucesso)
        #             ch.basic_ack(method.delivery_tag)
        #         else:
        #             print(self.msg_erro)
        #             ch.basic_reject(method.delivery_tag, requeue=False)
        #     else:
        #         ch.basic_reject(method.delivery_tag, requeue=False)
        # except StreamLostError as e:
        #     raise e
        # except ChannelWrongStateError as e:
        #     raise e
        # except Exception as e:
        #     print('ERROR: ' + str(e))
        #     ch.basic_reject(method.delivery_tag, requeue=False)


class BetterThanYesterdayFromNuvemFiscalDLConsumer(BasicQueueConsumer):

    exchanges = []

    queue_name = 'nuvem_fiscal_to_reprocess_dl'
    arguments = {
        'x-dead-letter-routing-key': 'nuvem_fiscal_to_reprocess',
        'x-dead-letter-exchange': ''
    }

    def __init__(self, *args, **kwargs):
        super().__init__(self.queue_name, exchanges=self.exchanges,
                         prefetch_size=16, arguments=self.arguments,
                         *args, **kwargs)

    def run(self):
        self.declare_and_consume(self.handle_message)

    def handle_message(self, ch, method, properties, body):
        pass
        # try:
        #     print('Mensagem reenviada para fila principal!')
        #     ch.basic_reject(method.delivery_tag, requeue=False)
        # except StreamLostError as e:
        #     raise e
        # except ChannelWrongStateError as e:
        #     raise e
        # except Exception as e:
        #     print('ERROR: ' + str(e))
        #     ch.basic_reject(method.delivery_tag, requeue=False)
