# from jjsystem.common import exception


def criar_centro_resultado_padrao(operation, created_by):
    centro_resultado_dict = {
        'domain_id': operation.entity.domain_id,
        'tarefa_id': operation.entity.id,
        'descricao': 'SETOR ADMINISTRATIVO',
        'created_by': created_by
    }
    operation.manager.api.centro_resultados().create(**centro_resultado_dict)


def criar_portador_padrao(operation, created_by):
    portador_dict = {
        'domain_id': operation.entity.domain_id,
        'tarefa_id': operation.entity.id,
        'tipo': 'INTERNO',
        'descricao': 'CONTA CAIXA',
        'padrao': True,
        'created_by': created_by
    }
    operation.manager.api.portadores().create(**portador_dict)


def criar_forma_pagto_dinheiro(operation, created_by):
    # codigo = '01'
    # descricao = 'Dinheiro'
    # forma_pagtos = operation.manager.api.formas_pagamento_sefaz().list(
    #     codigo=codigo, descricao=descricao)
    # if len(forma_pagtos) == 0:
    #     raise exception.NotFound(
    #         'Não foi possível encontrar a forma_pagamento_sefaz com ' +
    #         f'codigo={codigo} e descricao={descricao}')

    # cria forma_pagamento Dinheiro
    forma_pagto_dict = {
        'domain_id': operation.entity.domain_id,
        'tarefa_id': operation.entity.id,
        'codigo': 0,
        'nome': 'DINHEIRO',
        # 'forma_pagamento_sefaz_id': forma_pagtos[0].id,
        'created_by': created_by}
    operation.manager.api.forma_pagamentos().create(**forma_pagto_dict)


def criar_forma_pagto_pix(operation, created_by):
    # codigo = '17'
    # descricao = 'Pagamento Instantâneo (PIX)'
    # forma_pagtos = operation.manager.api.formas_pagamento_sefaz().list(
    #     codigo=codigo, descricao=descricao)
    # if len(forma_pagtos) == 0:
    #     raise exception.NotFound(
    #         'Não foi possível encontrar a forma_pagamento_sefaz com ' +
    #         f'codigo={codigo} e descricao={descricao}')

    # cria forma_pagamento (PIX)
    forma_pagto_dict = {
        'domain_id': operation.entity.domain_id,
        'tarefa_id': operation.entity.id,
        'codigo': -1,
        'nome': 'PIX',
        # 'forma_pagamento_sefaz_id': forma_pagtos[0].id,
        'created_by': created_by}
    operation.manager.api.forma_pagamentos().create(**forma_pagto_dict)
