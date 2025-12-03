
import uuid
import hashlib

from flask.globals import current_app
from datetime import datetime

from jjsystem.common import exception
from jjsystem.subsystem.token import manager
from jjsystem.common.subsystem import operation


class Create(operation.Operation):

    LIMIT_TOKENS = None

    def get_limit_tokens(self, domain):
        self.LIMIT_TOKENS = domain.application.settings.get('regras', {}).\
            get('limit_tokens', current_app.config['LIMIT_TOKENS'])

    def _check_tokens(self, user_id):
        limit = self.LIMIT_TOKENS
        tokens = self.manager.api.tokens().list(user_id=user_id)
        if len(tokens) >= limit:
            user_roles = \
                list(set(list(map(lambda x: x.role.name, self.user.grants))))
            reset_roles = ['Admin', 'Sysadmin', 'Suporte']
            can_reset = any(x in user_roles for x in reset_roles)

            error_msg = 'B!' if can_reset is True else ''

            if 'Sysadmin' not in user_roles:
                raise exception.BadRequest(
                    f'{error_msg}Limite de logins ativos atingido')

    def _remove_tokens(self, session, user_id):
        limit = self.LIMIT_TOKENS
        tokens = self.manager.api.tokens().list(user_id=user_id)
        tokens = sorted(tokens, key=lambda x: x.created_at, reverse=True)
        if len(tokens) >= limit:
            # lastest_token = tokens[0]
            if limit > 1:
                lastest_token_ids = list(map(lambda x: x.id, tokens[:limit-1]))
                lastest_token_ids = str(lastest_token_ids)
                lastest_token_ids = lastest_token_ids.replace('[', '(')
                lastest_token_ids = lastest_token_ids.replace(']', ')')
                lastest_token_ids = lastest_token_ids.replace('"', '\'')
            # se o limit for igual a 1 então tem que deletar todos os
            # tokens deste usuário para ele poder logar
            else:
                lastest_token_ids = "('')"

            query = """
                DELETE FROM token t
                WHERE t.user_id = '{}'
                    AND t.id NOT IN {}
            """.format(user_id, lastest_token_ids)
            session.execute(query)

    def pre(self, **kwargs):
        self.remove_tokens = kwargs.get('remove_tokens', False)
        self.natureza = kwargs.get('natureza', None)

        # FIXME(samueldmq): this method needs to receive the parameters
        # explicitly.
        if kwargs.get('user'):
            # FIXME(samueldmq): how to avoid someone simply passing the user
            # in the body and then having a valid token?

            # README (andr3) samueldmq, um pouco mais de informação da próxima
            # vez, por favor, essa validação é necessária para o registro de
            # domínio
            self.user = kwargs['user']
            domains = self.manager.api.domains().list(id=self.user.domain_id)
            if not domains:
                return False

            domain_id = domains[0].id
            self.get_limit_tokens(domain=domains[0])
        else:
            domain_name = kwargs.get('domain_name', None)
            username = kwargs.get('username', None)
            email = kwargs.get('email', None)
            password = kwargs.get('password', None)
            password_hash = kwargs.get('password_hash', None)

            # TODO(samueldmq): allow get by unique attrs
            domains = self.manager.api.domains().list(name=domain_name)

            if not domains:
                return False

            domain_id = domains[0].id
            self.get_limit_tokens(domain=domains[0])
            if password_hash is None:
                password_hash = hashlib.sha256(
                    password.encode('utf-8')).hexdigest()

            if (email is None):
                users = self.manager.api.users().list(
                    domain_id=domain_id, name=username, password=password_hash)
            else:
                users = self.manager.api.users().list(
                    domain_id=domain_id, email=email, password=password_hash)

            if not users:
                return False

            self.user = users[0]
            if self.user.active is False:
                raise exception.PreconditionFailed('Usuário não está ativo!')

        return self.user.is_stable()

    def do(self, session, **kwargs):
        # TODO(samueldmq): use self.user.id instead of self.user_id

        if self.remove_tokens:
            self._remove_tokens(session=session, user_id=self.user.id)

        self._check_tokens(self.user.id)

        token = self.driver.instantiate(
            id=uuid.uuid4().hex,
            created_by=self.user.id,
            created_at=datetime.now(),
            user_id=self.user.id,
            natureza=self.natureza)

        self.driver.create(token, session=session)

        return token


class Manager(manager.Manager):

    def __init__(self, driver):
        super().__init__(driver)
        self.create = Create(self)
