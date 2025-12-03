
class Message(object):
    '''Object for group attributes from rabbitmq message'''

    def __init__(self, type: str,
                 event_type: str,
                 routing_key: str,
                 payload: dict) -> None:
        self.type = type
        self.event_type = event_type
        self.routing_key = routing_key
        self.payload = payload

    def __str__(self) -> str:
        return 'Message(type={}, event_type={}, routing_key={}, payload={})'.\
            format(self.type, self.event_type, self.routing_key, self.payload)
