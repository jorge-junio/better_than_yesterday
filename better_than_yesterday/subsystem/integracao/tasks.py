
from flask.globals import current_app

from jjsystem.queue import ProducerQueue
from jjsystem.celery import celery, decide_on_run
from jjsystem.common.utils import to_json


@decide_on_run
@celery.task
def publish_queue_subroutine(info) -> None:
    api = current_app.api_handler.api()
    domain_id = info[0]
    payload = info[1]
    payload_json = to_json(payload)

    entity_name = payload.get('entity_name', None)
    domains = api.domains().list(id=domain_id)
    if len(domains) == 0 or entity_name is None:
        return

    routing_key_integration = '{}.{}.{}'.format(
        domain_id, 'queue_subroutine', entity_name)

    def publish(producer: ProducerQueue):
        producer.publish_request_entity('better_than_yesterday_integration',
                                        routing_key_integration,
                                        payload_json, 'queue_subroutine', 10)

    ProducerQueue().run(publish)
