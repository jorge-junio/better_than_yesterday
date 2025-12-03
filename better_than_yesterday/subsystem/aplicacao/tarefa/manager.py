from better_than_yesterday.subsystem.common.utils import remove_read_only_attributes
from jjsystem.common import exception
from jjsystem.common.subsystem import operation, manager
from better_than_yesterday.subsystem.aplicacao.tarefa.resource import \
    (Tarefa, TarefaContato, TarefaEndereco)
from jjsystem.subsystem.user.resource import User


class Create(operation.Create):

    def _validar_user(self, **user_data):
        domain_id = user_data.get('domain_id', None)
        email = user_data.get('email', None)
        name = user_data.get('name', None)
        # validar email
        users = self.manager.api.users().list(domain_id=domain_id, email=email)
        if len(users) > 0:
            raise exception.BadRequest(
                'Já existe um usuário cadastrado para este email.')
        # validar name
        users = self.manager.api.users().list(domain_id=domain_id, name=name)
        if len(users) > 0:
            raise exception.BadRequest(
                'Já existe um usuário cadastrado para este nome.')

    def _cadastrar_user(self, session, **user_data):
        self._validar_user(**user_data)
        roles = user_data.pop('roles', [])
        user = self.manager.api.users().create(session=session, **user_data)
        for role in roles:
            self.manager.api.grants().create(
                session=session,
                role_id=role.get('role_id', None),
                user_id=user.id)
        return user

    def pre(self, session, **kwargs):
        codigo = kwargs.get('codigo', None)
        domain_id = kwargs.get('domain_id', None)

        user_data = kwargs.pop('user', None)
        # cadastra o usuário
        if user_data is not None:
            user_id = user_data.pop('id', None)
            if user_id is None:
                user = self._cadastrar_user(session=session, **user_data)
                kwargs['user_id'] = user.id

        if codigo is None:
            kwargs['codigo'] = self.manager.api.domain_sequences().\
                get_nextval(id=domain_id, name=Tarefa.CODIGO_SEQUENCE)
        super().pre(session, **kwargs)
        return self.entity.is_stable()


class Update(operation.Update):

    def do(self, session, **kwargs):
        kwargs = remove_read_only_attributes(
            Tarefa.read_only_attributes,
            **kwargs)
        return super().do(session, **kwargs)


class List(operation.List):

    def do(self, session, **kwargs):
        query = session.query(Tarefa, User.name). \
            join(TarefaEndereco,
                 Tarefa.id == TarefaEndereco.tarefa_id,
                 isouter=True). \
            join(TarefaContato,
                 Tarefa.id == TarefaContato.tarefa_id,
                 isouter=True). \
            join(User, User.id == Tarefa.user_id, isouter=True)

        dict_compare = {"contatos.": TarefaContato,
                        "enderecos.": TarefaEndereco,
                        "user.": User}
        query = query.distinct()

        # trata o order_by de user para colocar as aspas, de modo que
        # o postgresql entenda que é uma tabela e não o user do postres
        order_by = kwargs.get('order_by', None)
        if order_by is not None:
            if 'user.' in order_by:
                kwargs['order_by'] = order_by.replace('user.', '"user".')

        kwargs['query'] = query
        kwargs['dict_compare'] = dict_compare
        kwargs['only_first_column'] = True
        return super().do(session=session, **kwargs)


# início das classes que gerenciam as settings do Tarefa
class UpdateSettings(operation.Update):

    def pre(self, session, id: str, **kwargs) -> bool:
        self.settings = kwargs
        if self.settings is None or not self.settings:
            raise exception.BadRequest("Erro! 'settings' está vazio.")
        return super().pre(session=session, id=id)

    def do(self, session, **kwargs):
        result = {}
        for key, value in self.settings.items():
            new_value = self.entity.update_setting(key, value)
            result[key] = new_value
        super().do(session)

        return result


class RemoveSettings(operation.Update):

    def pre(self, session, id: str, **kwargs) -> bool:
        self.keys = kwargs.get('keys', [])
        if not self.keys:
            raise exception.BadRequest(
                'Erro! A lista de "keys" está vazia.')
        super().pre(session, id=id)

        return self.entity.is_stable()

    def do(self, session, **kwargs):
        result = {}
        for key in self.keys:
            value = self.entity.remove_setting(key)
            result[key] = value
        super().do(session=session)

        return result


class GetSettingsByKeys(operation.Get):

    def pre(self, session, id, **kwargs):
        self.keys = kwargs.get('keys', [])
        if not self.keys:
            raise exception.BadRequest(
                'Erro! A lista de "keys" está vazia.')
        return super().pre(session, id=id)

    def do(self, session, **kwargs):
        entity = super().do(session=session)
        settings = {}
        for key in self.keys:
            value = entity.settings.get(key, None)
            if value is not None:
                settings[key] = value
        return settings


class Manager(manager.Manager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.create = Create(self)
        self.update = Update(self)
        self.list = List(self)
        # funções das settings
        self.update_settings = UpdateSettings(self)
        self.remove_settings = RemoveSettings(self)
        self.get_settings_by_keys = GetSettingsByKeys(self)

    def init_query(self, session, order_by, resource):
        query = session.query(Tarefa, Tarefa.id). \
            join(TarefaEndereco,
                 Tarefa.id == TarefaEndereco.tarefa_id,
                 isouter=True). \
            join(TarefaContato,
                 Tarefa.id == TarefaContato.tarefa_id,
                 isouter=True)
        return query
