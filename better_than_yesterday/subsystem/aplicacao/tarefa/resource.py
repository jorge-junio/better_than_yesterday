import json
import typing as t
from jjlocal.subsystem.common import endereco
from jjsystem.common import exception
from jjsystem.common.subsystem import entity
from jjsystem.database import db
from sqlalchemy import orm, UniqueConstraint


class Tarefa(entity.Entity, db.Model):

    CODIGO_SEQUENCE = 'tarefa_codigo_sq'

    attributes = ['domain_id', 'codigo', 'user_id',
                  'cpf_cnpj', 'doc_estrangeiro', 'rg_insc_est',
                  'nome_razao_social', 'apelido_nome_fantasia',
                  'observacao', 'data_nascimento']
    read_only_attributes = ['settings']
    attributes += entity.Entity.attributes
    attributes += read_only_attributes

    domain_id = db.Column(
        db.CHAR(32), db.ForeignKey('domain.id'), nullable=False)
    user_id = db.Column(
        db.CHAR(32), db.ForeignKey('user.id'), nullable=True, unique=True)
    user = orm.relationship('User', backref=orm.backref('tarefa_user'))
    codigo = db.Column(db.Numeric(10), db.Sequence(CODIGO_SEQUENCE),
                       nullable=False)
    cpf_cnpj = db.Column(db.CHAR(14), nullable=False)
    doc_estrangeiro = db.Column(db.CHAR(20), nullable=True)
    rg_insc_est = db.Column(db.String(20), nullable=True)
    nome_razao_social = db.Column(db.String(60), nullable=True)
    apelido_nome_fantasia = db.Column(db.String(60), nullable=True)
    observacao = db.Column(db.String(500), nullable=True)
    data_nascimento = db.Column(db.DateTime, nullable=True)

    _settings = db.Column('settings', db.Text, nullable=False,
                          server_default='{}')

    # embedded
    enderecos = orm.relationship(
        "TarefaEndereco", backref=orm.backref('tarefa_enderecos'),
        cascade='delete,delete-orphan,save-update')
    contatos = orm.relationship(
        "TarefaContato", backref=orm.backref('contatos_contatos'),
        cascade='delete,delete-orphan,save-update')

    __table_args__ = (
        UniqueConstraint(
            'domain_id', 'codigo', name='tarefa_domain_id_codigo_uk'),)

    def __init__(self, id, domain_id, codigo, user_id,
                 cpf_cnpj,
                 doc_estrangeiro=None, rg_insc_est=None, nome_razao_social=None,
                 apelido_nome_fantasia=None, observacao=None,
                 data_nascimento=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.domain_id = domain_id
        self.codigo = codigo
        self.user_id = user_id
        self.cpf_cnpj = cpf_cnpj
        self.doc_estrangeiro = doc_estrangeiro
        self.rg_insc_est = rg_insc_est
        self.nome_razao_social = nome_razao_social
        self.apelido_nome_fantasia = apelido_nome_fantasia
        self.observacao = observacao
        self.data_nascimento = data_nascimento

    # começo das funções das settings
    def _has_setting(self, key: str) -> bool:
        return self.settings.get(key) is not None

    def _save_settings(self, settings: dict):
        self._settings = json.dumps(settings, default=str)

    def remove_setting(self, key: str):
        if not self._has_setting(key):
            raise exception.BadRequest(f"Erro! Setting {key} not exists")

        settings = self.settings
        value = settings.pop(key)
        self._save_settings(settings)

        return value

    def update_setting(self, key: str, value: t.Any):
        settings = self.settings
        settings[key] = value
        self._save_settings(settings)
        return value
    # final das funções das settings

    @property
    def settings(self):
        try:
            settings_str = '{}' if self._settings is None else self._settings
            return json.loads(settings_str)
        except Exception:
            return {}

    @classmethod
    def collection(cls):
        return 'tarefaes'

    @classmethod
    def embedded(cls):
        return ['enderecos', 'contatos']


class TarefaEndereco(endereco.resource.Endereco, db.Model):

    attributes = ['id', 'municipio_nome', 'municipio_sigla_uf', 'pais_id']
    attributes += endereco.resource.Endereco.attributes
    municipio_id = db.Column(
        db.CHAR(32), db.ForeignKey('municipio.id'), nullable=False)
    municipio = orm.relationship(
        'Municipio', backref=orm.backref('tarefa_municipio'))
    pais_id = db.Column(
        db.CHAR(32), db.ForeignKey('pais.id'), nullable=True)
    pais = orm.relationship(
        'Pais', backref=orm.backref('tarefa_endereco_pais'))

    tarefa_id = db.Column(
        db.CHAR(32), db.ForeignKey("tarefa.id"), nullable=False)

    def __init__(self, id, tarefa_id, logradouro, numero, bairro,
                 municipio_id, cep, complemento=None, ponto_referencia=None,
                 pais_id=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, logradouro, numero, bairro, municipio_id, cep,
                         complemento, ponto_referencia, active, created_at,
                         created_by, updated_at, updated_by, tag)
        self.tarefa_id = tarefa_id
        self.pais_id = pais_id

    @property
    def municipio_nome(self):
        if self.municipio is not None:
            return self.municipio.nome
        else:
            return None

    @property
    def municipio_sigla_uf(self):
        if self.municipio is not None:
            return self.municipio.sigla_uf
        else:
            return None


class TarefaContato(entity.Entity, db.Model):

    attributes = ['id', 'contato', 'tag']

    tarefa_id = db.Column(
        db.CHAR(32), db.ForeignKey("tarefa.id"), nullable=False)
    contato = db.Column(db.String(100), nullable=False)

    def __init__(self, id, tarefa_id, contato,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.tarefa_id = tarefa_id
        self.contato = contato
