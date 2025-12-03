from jjsystem.database import db
from jjsystem.common.subsystem import entity


class ErroConsumoRabbitmq(entity.Entity, db.Model):
    attributes = ['tipo_mensagem', 'error', 'properties', 'payload']
    attributes += entity.Entity.attributes

    message_type = db.Column(db.String(80), nullable=False)
    error = db.Column(db.String(2000), nullable=False)
    properties = db.Column(db.String(1000), nullable=False)
    payload = db.Column(db.TEXT, nullable=False)

    def __init__(self, id, message_type, error, properties, payload,
                 active=True, created_at=None,
                 created_by=None, updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by, updated_at,
                         updated_by, tag)
        self.message_type = message_type
        self.error = error
        self.properties = properties
        self.payload = payload

    @classmethod
    def individual(cls):
        return 'erro_consumo_rabbitmq'
