QUERY = """
SELECT query.entity, query.total, d."name", d.application_id, a."name", d.id, d.active
FROM (
        SELECT 'caixa' AS entity, count(id) AS total, domain_id
        FROM caixa
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'caixa_detalhe_fechamento' AS entity, count(id) AS total, domain_id
        FROM caixa_detalhe_fechamento
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'caixa_evento' AS entity, count(aux.id) AS total, domain_id
        FROM caixa_evento aux
        	JOIN caixa c ON c.id = aux.caixa_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'caixa_item' AS entity, count(id) AS total, domain_id
        FROM caixa_item
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'catalogo' AS entity, count(id) AS total, domain_id
        FROM catalogo
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'catalogo_grupo' AS entity, count(aux.id) AS total, domain_id
        FROM catalogo_grupo aux
        	JOIN catalogo c ON c.id = aux.catalogo_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'catalogo_produto' AS entity, count(aux.id) AS total, domain_id
        FROM catalogo_produto aux
        	JOIN catalogo c ON c.id = aux.catalogo_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'centro_resultado' AS entity, count(id) AS total, domain_id
        FROM centro_resultado
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'certificado_digital' AS entity, count(id) AS total, domain_org_id AS domain_id
        FROM certificado_digital
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'cliente' AS entity, count(id) AS total, domain_id
        FROM cliente
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'cliente_condicao_pagamento_bloqueado' AS entity, count(aux.id) AS total, domain_id
        FROM cliente_condicao_pagamento_bloqueado aux
        	JOIN cliente c ON c.id = aux.cliente_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'cliente_cpf_cnpj_autorizado' AS entity, count(aux.id) AS total, domain_id
        FROM cliente_cpf_cnpj_autorizado aux
        	JOIN cliente c ON c.id = aux.cliente_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'cliente_limite_credito_evento' AS entity, count(aux.id) AS total, domain_id
        FROM cliente_limite_credito_evento aux
        	JOIN cliente c ON c.id = aux.cliente_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'codigo_seguranca_contribuinte' AS entity, count(id) AS total, domain_org_id AS domain_id
        FROM codigo_seguranca_contribuinte
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'condicao_pagamento' AS entity, count(id) AS total, domain_id
        FROM condicao_pagamento
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'condicao_pagamento_parcela' AS entity, count(aux.id) AS total, domain_id
        FROM condicao_pagamento_parcela aux
        	JOIN condicao_pagamento cp ON cp.id = aux.condicao_pagamento_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'conta_pagar' AS entity, count(id) AS total, domain_id
        FROM conta_pagar
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'conta_pagar_evento' AS entity, count(aux.id) AS total, domain_id
        FROM conta_pagar_evento aux
        	JOIN conta_pagar cp ON cp.id = aux.conta_pagar_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'conta_pagar_pagto' AS entity, count(aux.id) AS total, domain_id
        FROM conta_pagar_pagto aux
        	JOIN conta_pagar_parcela cpp ON cpp.id = aux.conta_pagar_parcela_id
        	JOIN conta_pagar cp ON cp.id = cpp.conta_pagar_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'conta_pagar_parcela' AS entity, count(aux.id) AS total, domain_id
        FROM conta_pagar_parcela aux
        	JOIN conta_pagar cp ON cp.id = aux.conta_pagar_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'conta_pagar_parcela_evento' AS entity, count(aux.id) AS total, domain_id
        FROM conta_pagar_parcela_evento aux
        	JOIN conta_pagar_parcela cpp ON cpp.id = aux.conta_pagar_parcela_id
        	JOIN conta_pagar cp ON cp.id = cpp.conta_pagar_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'conta_receber' AS entity, count(id) AS total, domain_id
        FROM conta_receber
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'conta_receber_evento' AS entity, count(aux.id) AS total, domain_id
        FROM conta_receber_evento aux
        	JOIN conta_receber cr ON cr.id = aux.conta_receber_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'conta_receber_pagto' AS entity, count(aux.id) AS total, domain_id
        FROM conta_receber_pagto aux
        	JOIN conta_receber_parcela crp ON crp.id = aux.conta_receber_parcela_id
        	JOIN conta_receber cr ON cr.id = crp.conta_receber_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'conta_receber_parcela' AS entity, count(aux.id) AS total, domain_id
        FROM conta_receber_parcela aux
        	JOIN conta_receber cr ON cr.id = aux.conta_receber_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'conta_receber_parcela_evento' AS entity, count(aux.id) AS total, domain_id
        FROM conta_receber_parcela_evento aux
        	JOIN conta_receber_parcela crp ON crp.id = aux.conta_receber_parcela_id
        	JOIN conta_receber cr ON cr.id = crp.conta_receber_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'domain' AS entity, count(id) AS total, id AS domain_id
        FROM domain
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY id
    UNION
        SELECT 'domain_address' AS entity, count(id) AS total, domain_id
        FROM domain_address
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'domain_and_table_sequence' AS entity, count(id) AS total, domain_id
        FROM domain_and_table_sequence
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'domain_contact' AS entity, count(id) AS total, domain_id
        FROM domain_contact
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'domain_org' AS entity, count(id) AS total, id AS domain_id
        FROM domain_org
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY id
    UNION
        SELECT 'domain_sequence' AS entity, count(id) AS total, domain_id
        FROM domain_sequence
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'equipe_venda' AS entity, count(id) AS total, domain_id
        FROM equipe_venda
        GROUP BY domain_id
    UNION
        SELECT 'equipe_venda_catalogo' AS entity, count(aux.id) AS total, domain_id
        FROM equipe_venda_catalogo aux
        	JOIN equipe_venda ev ON ev.id = aux.equipe_venda_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'erro_integracao' AS entity, count(id) AS total, domain_id
        FROM erro_integracao
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'erro_integracao_externa' AS entity, count(aux.id) AS total, domain_id
        FROM erro_integracao_externa aux
        	JOIN log_erro_integracao_externa leie ON leie.id = aux.log_erro_integracao_externa_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'fabricante' AS entity, count(aux.id) AS total, domain_id
        FROM fabricante aux
        	JOIN parceiro p ON p.id = aux.id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'file_infosys' AS entity, count(id) AS total, domain_id
        FROM file_infosys
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'forma_pagamento' AS entity, count(id) AS total, domain_id
        FROM forma_pagamento
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'tarefa' AS entity, count(id) AS total, domain_id
        FROM tarefa
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'tarefa_limite_credito_evento' AS entity, count(aux.id) AS total, domain_id
        FROM tarefa_limite_credito_evento aux
        	JOIN tarefa f ON f.id = aux.tarefa_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'grupo' AS entity, count(id) AS total, domain_id
        FROM grupo
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'image' AS entity, count(aux.id) AS total, domain_id
        FROM image aux
        	JOIN file_infosys fi ON fi.id = aux.id
        GROUP BY domain_id
    UNION
        SELECT 'instituicao_pagamento' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM instituicao_pagamento aux
        	JOIN domain_org dorg ON dorg.id = aux.domain_org_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'justificativa' AS entity, count(id) AS total, domain_id
        FROM justificativa
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'movimentacao_financeira' AS entity, count(id) AS total, domain_id
        FROM movimentacao_financeira
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'movimentacao_financeira_evento' AS entity, count(aux.id) AS total, domain_id
        FROM movimentacao_financeira_evento aux
        	JOIN movimentacao_financeira mf ON mf.id = aux.movimentacao_financeira_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'natureza_financeira' AS entity, count(id) AS total, domain_id
        FROM natureza_financeira
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'natureza_operacao' AS entity, count(id) AS total, domain_org_id AS domain_id
        FROM natureza_operacao
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce' AS entity, count(id) AS total, domain_org_id AS domain_id
        FROM nfce
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_autxml' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfce_autxml aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_cana_deduc' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfce_cana_deduc aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_cana_fordia' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfce_cana_fordia aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_cobr_dup' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfce_cobr_dup aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_evento' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfce_evento aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_evento_sefaz' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfce_evento_sefaz aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_ide_nfref' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfce_ide_nfref aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_inconsistencia' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfce_inconsistencia aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_infadic_obscont' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfce_infadic_obscont aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_infadic_obsfisco' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfce_infadic_obsfisco aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_infadic_procref' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfce_infadic_procref aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_item' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfce_item aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_item_prod_arma' AS entity, count(aux2.id), domain_org_id AS domain_id
        FROM nfce_item_prod_arma aux2
        	JOIN nfce_item aux ON aux.id = aux2.nfce_item_id
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux2.created_at IS NOT NULL AND (aux2.created_at > \'{de}\' AND aux2.created_at < \'{ate}\'))
		    OR (aux2.updated_at IS NOT NULL AND (aux2.updated_at > \'{de}\' AND aux2.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_item_prod_detexport' AS entity, count(aux2.id), domain_org_id AS domain_id
        FROM nfce_item_prod_detexport aux2
        	JOIN nfce_item aux ON aux.id = aux2.nfce_item_id
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux2.created_at IS NOT NULL AND (aux2.created_at > \'{de}\' AND aux2.created_at < \'{ate}\'))
		    OR (aux2.updated_at IS NOT NULL AND (aux2.updated_at > \'{de}\' AND aux2.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_item_prod_di' AS entity, count(aux2.id), domain_org_id AS domain_id
        FROM nfce_item_prod_di aux2
        	JOIN nfce_item aux ON aux.id = aux2.nfce_item_id
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux2.created_at IS NOT NULL AND (aux2.created_at > \'{de}\' AND aux2.created_at < \'{ate}\'))
		    OR (aux2.updated_at IS NOT NULL AND (aux2.updated_at > \'{de}\' AND aux2.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_item_prod_di_adi' AS entity, count(aux3.id), domain_org_id AS domain_id
        FROM nfce_item_prod_di_adi aux3
        	JOIN nfce_item_prod_di aux2 ON aux2.id = aux3.nfce_item_prod_di_id
        	JOIN nfce_item aux ON aux.id = aux2.nfce_item_id
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux3.created_at IS NOT NULL AND (aux3.created_at > \'{de}\' AND aux3.created_at < \'{ate}\'))
		    OR (aux3.updated_at IS NOT NULL AND (aux3.updated_at > \'{de}\' AND aux3.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_item_prod_rastro' AS entity, count(aux2.id), domain_org_id AS domain_id
        FROM nfce_item_prod_rastro aux2
        	JOIN nfce_item aux ON aux.id = aux2.nfce_item_id
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux2.created_at IS NOT NULL AND (aux2.created_at > \'{de}\' AND aux2.created_at < \'{ate}\'))
		    OR (aux2.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux2.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_pag_detpag' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfce_pag_detpag aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_pedido' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfce_pedido aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_transp_reboque' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfce_transp_reboque aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_transp_vol' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfce_transp_vol aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfe aux
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_autxml' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfe_autxml aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_cana_deduc' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfe_cana_deduc aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_cana_fordia' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfe_cana_fordia aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_cobr_dup' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfe_cobr_dup aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_evento' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfe_evento aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_evento_sefaz' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfe_evento_sefaz aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_ide_nfref' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfe_ide_nfref aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_inconsistencia' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfe_inconsistencia aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_infadic_obscont' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfe_infadic_obscont aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_infadic_obsfisco' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfe_infadic_obsfisco aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_infadic_procref' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfe_infadic_procref aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_item' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfe_item aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_item_prod_arma' AS entity, count(aux2.id), domain_org_id AS domain_id
        FROM nfe_item_prod_arma aux2
        	JOIN nfe_item aux ON aux.id = aux2.nfe_item_id
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux2.created_at IS NOT NULL AND (aux2.created_at > \'{de}\' AND aux2.created_at < \'{ate}\'))
		    OR (aux2.updated_at IS NOT NULL AND (aux2.updated_at > \'{de}\' AND aux2.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_item_prod_detexport' AS entity, count(aux2.id), domain_org_id AS domain_id
        FROM nfe_item_prod_detexport aux2
        	JOIN nfe_item aux ON aux.id = aux2.nfe_item_id
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux2.created_at IS NOT NULL AND (aux2.created_at > \'{de}\' AND aux2.created_at < \'{ate}\'))
		    OR (aux2.updated_at IS NOT NULL AND (aux2.updated_at > \'{de}\' AND aux2.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_item_prod_di' AS entity, count(aux2.id), domain_org_id AS domain_id
        FROM nfe_item_prod_di aux2
        	JOIN nfe_item aux ON aux.id = aux2.nfe_item_id
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux2.created_at IS NOT NULL AND (aux2.created_at > \'{de}\' AND aux2.created_at < \'{ate}\'))
		    OR (aux2.updated_at IS NOT NULL AND (aux2.updated_at > \'{de}\' AND aux2.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_item_prod_di_adi' AS entity, count(aux3.id), domain_org_id AS domain_id
        FROM nfe_item_prod_di_adi aux3
        	JOIN nfe_item_prod_di aux2 ON aux2.id = aux3.nfe_item_prod_di_id
        	JOIN nfe_item aux ON aux.id = aux2.nfe_item_id
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux3.created_at IS NOT NULL AND (aux3.created_at > \'{de}\' AND aux3.created_at < \'{ate}\'))
		    OR (aux3.updated_at IS NOT NULL AND (aux3.updated_at > \'{de}\' AND aux3.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_item_prod_rastro' AS entity, count(aux2.id), domain_org_id AS domain_id
        FROM nfe_item_prod_rastro aux2
        	JOIN nfe_item aux ON aux.id = aux2.nfe_item_id
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux2.created_at IS NOT NULL AND (aux2.created_at > \'{de}\' AND aux2.created_at < \'{ate}\'))
		    OR (aux2.updated_at IS NOT NULL AND (aux2.updated_at > \'{de}\' AND aux2.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_pag_detpag' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfe_pag_detpag aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_pedido' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfe_pedido aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_pedido_produto' AS entity, count(aux2.id), domain_org_id AS domain_id
        FROM nfe_pedido_produto aux2
        	JOIN nfe_pedido aux ON aux.id = aux2.nfe_pedido_id
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux2.created_at IS NOT NULL AND (aux2.created_at > \'{de}\' AND aux2.created_at < \'{ate}\'))
		    OR (aux2.updated_at IS NOT NULL AND (aux2.updated_at > \'{de}\' AND aux2.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_transp_reboque' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfe_transp_reboque aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_transp_vol' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM nfe_transp_vol aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'parceiro' AS entity, count(id) AS total, domain_id
        FROM parceiro
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'pedido' AS entity, count(id) AS total, domain_id
        FROM pedido
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'pedido_integracao' AS entity, count(id) AS total, domain_id
        FROM pedido_integracao
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'pedido_integracao_evento' AS entity, count(aux.id) AS total, domain_id
        FROM pedido_integracao_evento aux
        	JOIN pedido_integracao pint ON pint.id = aux.pedido_integracao_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'pedido_nfce' AS entity, count(id) AS total, domain_id
        FROM pedido_nfce
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'pedido_nfce_evento' AS entity, count(aux.id) AS total, domain_id
        FROM pedido_nfce_evento aux
        	JOIN pedido_nfce pn ON pn.id = aux.pedido_nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'pedido_nfce_forma_pagamento' AS entity, count(aux.id) AS total, domain_id
        FROM pedido_nfce_forma_pagamento aux
        	JOIN pedido_nfce pn ON pn.id = aux.pedido_nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'pedido_nfe' AS entity, count(id) AS total, domain_id
        FROM pedido_nfe
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'pedido_nfe_evento' AS entity, count(aux.id) AS total, domain_id
        FROM pedido_nfe_evento aux
        	JOIN pedido_nfe pn ON pn.id = aux.pedido_nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'pedido_nfe_forma_pagamento' AS entity, count(aux.id) AS total, domain_id
        FROM pedido_nfe_forma_pagamento aux
        	JOIN pedido_nfe pn ON pn.id = aux.pedido_nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'pedido_pre_pedido' AS entity, count(aux.id) AS total, domain_id
        FROM pedido_pre_pedido aux
        	JOIN pedido p ON p.id = aux.pedido_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'pedido_produto' AS entity, count(aux.id) AS total, domain_id
        FROM pedido_produto aux
        	JOIN pedido p ON p.id = aux.pedido_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'portador' AS entity, count(id) AS total, domain_id
        FROM portador
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'portaria' AS entity, count(id) AS total, domain_org_id AS domain_id
        FROM portaria
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'pre_cliente' AS entity, count(id) AS total, domain_id
        FROM pre_cliente
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'pre_cliente_evento' AS entity, count(aux.id) AS total, domain_id
        FROM pre_cliente_evento aux
        	JOIN pre_cliente pc ON pc.id = aux.pre_cliente_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'pre_pedido' AS entity, count(id) AS total, domain_id
        FROM pre_pedido
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'pre_pedido_evento' AS entity, count(aux.id) AS total, domain_id
        FROM pre_pedido_evento aux
        	JOIN pre_pedido pp ON pp.id = aux.pre_pedido_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'produto' AS entity, count(id) AS total, domain_id
        FROM produto
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'produto_entrada_fiscal' AS entity, count(id) AS total, domain_org_id AS domain_id
        FROM produto_entrada_fiscal
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'produto_entrada_fiscal_evento' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM produto_entrada_fiscal_evento aux
        	JOIN produto_entrada_fiscal pef ON pef.id = aux.produto_entrada_fiscal_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'produto_entrada_fiscal_produto_fiscal' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM produto_entrada_fiscal_produto_fiscal aux
        	JOIN produto_entrada_fiscal pef ON pef.id = aux.produto_entrada_fiscal_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'produto_estoque_evento' AS entity, count(aux.id) AS total, domain_id
        FROM produto_estoque_evento aux
        	JOIN produto p ON p.id = aux.produto_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'produto_fiscal' AS entity, count(id) AS total, domain_org_id AS domain_id
        FROM produto_fiscal
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'produto_fiscal_cbenef' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM produto_fiscal_cbenef aux
        	JOIN produto_fiscal pf ON pf.id = aux.produto_fiscal_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'produto_fiscal_regra_fiscal' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM produto_fiscal_regra_fiscal aux
        	JOIN produto_fiscal pf ON pf.id = aux.produto_fiscal_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'produto_fiscal_mva' AS entity, count(aux.id) AS total, domain_org_id AS domain_id
        FROM produto_fiscal_mva aux
        	JOIN produto_fiscal pf ON pf.id = aux.produto_fiscal_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'produto_tarefa' AS entity, count(aux.id) AS total, domain_id
        FROM produto_tarefa aux
        	JOIN produto p ON p.id = aux.produto_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'produto_imagem' AS entity, count(aux.id) AS total, domain_id
        FROM produto_imagem aux
        	JOIN produto p ON p.id = aux.produto_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'produto_pre_entrada' AS entity, count(id) AS total, domain_id
        FROM produto_pre_entrada
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'produto_pre_entrada_evento' AS entity, count(aux.id) AS total, domain_id
        FROM produto_pre_entrada_evento aux
        	JOIN produto_pre_entrada ppe ON ppe.id = aux.produto_pre_entrada_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'produto_tabela_preco' AS entity, count(aux.id) AS total, domain_id
        FROM produto_tabela_preco aux
        	JOIN produto p ON p.id = aux.produto_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'promocao_produto' AS entity, count(id) AS total, domain_id
        FROM promocao_produto
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'promocao_produto_evento' AS entity, count(aux.id) AS total, domain_id
        FROM promocao_produto_evento aux
        	JOIN promocao_produto pp ON pp.id = aux.promocao_produto_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'promocao_produto_produto' AS entity, count(aux.id) AS total, domain_id
        FROM promocao_produto_produto aux
        	JOIN promocao_produto pp ON pp.id = aux.promocao_produto_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'ree' AS entity, count(id) AS total, domain_id
        FROM ree
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'ree_evento' AS entity, count(aux.id) AS total, domain_id
        FROM ree_evento aux
        	JOIN ree r ON r.id = aux.ree_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'ree_produto' AS entity, count(aux.id) AS total, domain_id
        FROM ree_produto aux
        	JOIN ree r ON r.id = aux.ree_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'regra_fiscal' AS entity, count(id) AS total, domain_org_id AS domain_id
        FROM regra_fiscal
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'rse' AS entity, count(id) AS total, domain_id
        FROM rse
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'rse_evento' AS entity, count(aux.id) AS total, domain_id
        FROM rse_evento aux
        	JOIN rse r ON r.id = aux.rse_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'rse_produto' AS entity, count(aux.id) AS total, domain_id
        FROM rse_produto aux
        	JOIN rse r ON r.id = aux.rse_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'serie_fiscal' AS entity, count(id) AS total, domain_org_id AS domain_id
        FROM serie_fiscal
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'supervisor' AS entity, count(aux.id) AS total, domain_id
        FROM supervisor aux
        	JOIN parceiro p ON p.id = aux.id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'tabela_preco' AS entity, count(id) AS total, domain_id
        FROM tabela_preco
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'tag' AS entity, count(id) AS total, domain_id
        FROM tag
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'terminal' AS entity, count(id) AS total, domain_id
        FROM terminal
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'terminal_operador' AS entity, count(aux.id) AS total, domain_id
        FROM terminal_operador aux
        	JOIN terminal t ON t.id = aux.terminal_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'timeline_event' AS entity, count(id) AS total, domain_id
        FROM timeline_event
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'timeline_event_user' AS entity, count(aux.id) AS total, domain_id
        FROM timeline_event_user aux
        	JOIN timeline_event te ON te.id = aux.timeline_event_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'tipo_operacao' AS entity, count(id) AS total, domain_org_id AS domain_id
        FROM tipo_operacao
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'token' AS entity, count(aux.id) AS total, domain_id
        FROM "token" aux
			JOIN "user" u ON u.id = aux.user_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'uficms' AS entity, count(id) AS total, domain_org_id AS domain_id
        FROM uficms
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'unidade' AS entity, count(id) AS total, domain_id
        FROM unidade
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'user' AS entity, count(id) AS total, domain_id
        FROM "user"
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'vendedor' AS entity, count(id) AS total, domain_id
        FROM vendedor
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'vendedor_cliente' AS entity, count(aux.id) AS total, domain_id
        FROM vendedor_cliente aux
        	JOIN vendedor v ON v.id = aux.vendedor_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
    UNION
        SELECT 'vendedor_perde_ganha_evento' AS entity, count(aux.id) AS total, domain_id
        FROM vendedor_perde_ganha_evento aux
        	JOIN vendedor v ON v.id = aux.vendedor_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_id
) AS query
JOIN "domain" d ON d.id = query.domain_id
JOIN application a ON a.id = d.application_id
ORDER BY query.domain_id, query.entity;
"""  # noqa