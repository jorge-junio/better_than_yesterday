import os

import jjlocal
import jjsystem

from flask_cors import CORS

from jjsystem import database
from jjsystem.celery import celery
from jjsystem.system import System

from better_than_yesterday.subsystem.integracao.consumer import (
    RabbitmqConsumer)
from better_than_yesterday.resources import SYSADMIN_EXCLUSIVE_POLICIES, \
    SYSADMIN_RESOURCES, USER_RESOURCES
from better_than_yesterday._version import (
    version as better_than_yesterday_version)
# from datetime import datetime
from better_than_yesterday._packages import packages


system = System('better_than_yesterday',
                packages,
                USER_RESOURCES,
                SYSADMIN_RESOURCES,
                SYSADMIN_EXCLUSIVE_POLICIES)


class SystemFlask(jjsystem.SystemFlask):

    def __init__(self):
        super().__init__(system,
                         jjlocal.system)

    # def _configure_keep_alive(self):
    #     from werkzeug.serving import WSGIRequestHandler
    #     WSGIRequestHandler.protocol_version = "HTTP/1.1"

    def configure(self):
        # self._configure_keep_alive()

        origins_urls = os.environ.get('ORIGINS_URLS', '*')
        CORS(self, resources={r'/*': {'origins': origins_urls}})

        self.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        better_than_yesterday_database_uri = os.getenv(
            'BETTER_THAN_YESTERDAY_DATABASE_URI', None)
        if better_than_yesterday_database_uri is None:
            raise Exception(
                'BETTER_THAN_YESTERDAY_DATABASE_URI not defined in enviroment.')
        else:
            # URL os enviroment example for Postgres
            # export BETTER_THAN_YESTERDAY_DATABASE_URI=
            # mysql+pymysql://root:mysql@localhost:3306/jjlocal
            self.config['SQLALCHEMY_DATABASE_URI'] = (
                better_than_yesterday_database_uri)

        # Configurando a fila
        self.config['JJSYSTEM_QUEUE_URL'] = \
            os.getenv('BETTER_THAN_YESTERDAY_QUEUE_URL', None)
        self.config['JJSYSTEM_QUEUE_PORT'] = \
            os.getenv('BETTER_THAN_YESTERDAY_QUEUE_PORT', None)
        self.config['JJSYSTEM_QUEUE_VIRTUAL_HOST'] = \
            os.getenv('BETTER_THAN_YESTERDAY_QUEUE_VIRTUAL_HOST', None)
        self.config['JJSYSTEM_QUEUE_USERNAME'] = \
            os.getenv('BETTER_THAN_YESTERDAY_QUEUE_USERNAME', None)
        self.config['JJSYSTEM_QUEUE_PASSWORD'] = \
            os.getenv('BETTER_THAN_YESTERDAY_QUEUE_PASSWORD', None)

        self.config['CELERY_BROKER_URL'] = \
            os.getenv('CELERY_BROKER_URL', None)

        self.config['USE_WORKER'] = \
            os.getenv('BETTER_THAN_YESTERDAY_USE_WORKER', False) == 'True'

        # Configurando api_fiscal
        self.config['API_FISCAL'] = os.getenv('API_FISCAL', 'PRODUCAO')

        # Configurando limitação de acessos por usuário
        self.config['LIMIT_TOKENS'] = int(os.getenv('LIMIT_TOKENS', 1000))

    def version(self):
        return better_than_yesterday_version

    def init_database(self):
        database.db.init_app(self)
        with self.app_context():
            database.migrate.init_app(self, database.db)

    def configure_celery_consumer(self):
        with self.app_context():
            celery.steps['consumer'].add(RabbitmqConsumer)


def create_app() -> SystemFlask:
    app = SystemFlask()
    return app


def create_api() -> SystemFlask:
    app = SystemFlask()
    app.init_scheduler()
    app.configure_celery()
    return app


def create_worker():
    app = SystemFlask()
    app.configure_celery()
    app.app_context().push()
    return jjsystem.celery.celery


# def create_worker_integration():
#     app = SystemFlask()

#     app.configure_celery()
#     app.app_context().push()
#     with app.app_context():
#         print(app.version())
#         try:
#             consumer = BetterThanYesterdayFromIntegrationConsumer()
#             consumer.run()
#         except Exception as e:
#             print(str(datetime.now()) + ' - ' + str(e))
#             return create_worker_integration()


# def create_worker_integration_dl():
#     app = SystemFlask()
#     app.app_context().push()
#     with app.app_context():
#         print(app.version())
#         try:
#             consumer = BetterThanYesterdayFromIntegrationDLConsumer()
#             consumer.run()
#         except Exception as e:
#             print(str(datetime.now()) + ' - ' + str(e))
#             return create_worker_integration()


# def create_worker_nuvem_fiscal_reprocess():
#     app = SystemFlask()

#     app.configure_celery()
#     app.app_context().push()
#     with app.app_context():
#         print(app.version())
#         try:
#             consumer = BetterThanYesterdayFromNuvemFiscalConsumer()
#             consumer.run()
#         except Exception as e:
#             print(str(datetime.now()) + ' - ' + str(e))
#             return create_worker_nuvem_fiscal_reprocess()


# def create_worker_nuvem_fiscal_reprocess_dl():
#     app = SystemFlask()
#     app.app_context().push()
#     with app.app_context():
#         print(app.version())
#         try:
#             consumer = BetterThanYesterdayFromNuvemFiscalDLConsumer()
#             consumer.run()
#         except Exception as e:
#             print(str(datetime.now()) + ' - ' + str(e))
#             return create_worker_nuvem_fiscal_reprocess_dl()
