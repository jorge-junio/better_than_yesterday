QUERY = """
SELECT query.entity, query.total
FROM (
        SELECT 'caixa' AS entity, count(id) AS total
        FROM caixa
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'caixa_detalhe_fechamento' AS entity, count(id) AS total
        FROM caixa_detalhe_fechamento
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'caixa_evento' AS entity, count(aux.id) AS total
        FROM caixa_evento aux
        	JOIN caixa c ON c.id = aux.caixa_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'caixa_item' AS entity, count(id) AS total
        FROM caixa_item
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'catalogo' AS entity, count(id) AS total
        FROM catalogo
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'catalogo_grupo' AS entity, count(aux.id) AS total
        FROM catalogo_grupo aux
        	JOIN catalogo c ON c.id = aux.catalogo_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'catalogo_produto' AS entity, count(aux.id) AS total
        FROM catalogo_produto aux
        	JOIN catalogo c ON c.id = aux.catalogo_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'centro_resultado' AS entity, count(id) AS total
        FROM centro_resultado
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'certificado_digital' AS entity, count(id) AS total
        FROM certificado_digital
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'cliente' AS entity, count(id) AS total
        FROM cliente
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'cliente_condicao_pagamento_bloqueado' AS entity, count(aux.id) AS total
        FROM cliente_condicao_pagamento_bloqueado aux
        	JOIN cliente c ON c.id = aux.cliente_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'cliente_cpf_cnpj_autorizado' AS entity, count(aux.id) AS total
        FROM cliente_cpf_cnpj_autorizado aux
        	JOIN cliente c ON c.id = aux.cliente_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'cliente_limite_credito_evento' AS entity, count(aux.id) AS total
        FROM cliente_limite_credito_evento aux
        	JOIN cliente c ON c.id = aux.cliente_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'codigo_seguranca_contribuinte' AS entity, count(id) AS total
        FROM codigo_seguranca_contribuinte
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'condicao_pagamento' AS entity, count(id) AS total
        FROM condicao_pagamento
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'condicao_pagamento_parcela' AS entity, count(aux.id) AS total
        FROM condicao_pagamento_parcela aux
        	JOIN condicao_pagamento cp ON cp.id = aux.condicao_pagamento_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'conta_pagar' AS entity, count(id) AS total
        FROM conta_pagar
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'conta_pagar_evento' AS entity, count(aux.id) AS total
        FROM conta_pagar_evento aux
        	JOIN conta_pagar cp ON cp.id = aux.conta_pagar_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'conta_pagar_pagto' AS entity, count(aux.id) AS total
        FROM conta_pagar_pagto aux
        	JOIN conta_pagar_parcela cpp ON cpp.id = aux.conta_pagar_parcela_id
        	JOIN conta_pagar cp ON cp.id = cpp.conta_pagar_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'conta_pagar_parcela' AS entity, count(aux.id) AS total
        FROM conta_pagar_parcela aux
        	JOIN conta_pagar cp ON cp.id = aux.conta_pagar_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'conta_pagar_parcela_evento' AS entity, count(aux.id) AS total
        FROM conta_pagar_parcela_evento aux
        	JOIN conta_pagar_parcela cpp ON cpp.id = aux.conta_pagar_parcela_id
        	JOIN conta_pagar cp ON cp.id = cpp.conta_pagar_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'conta_receber' AS entity, count(id) AS total
        FROM conta_receber
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'conta_receber_evento' AS entity, count(aux.id) AS total
        FROM conta_receber_evento aux
        	JOIN conta_receber cr ON cr.id = aux.conta_receber_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'conta_receber_pagto' AS entity, count(aux.id) AS total
        FROM conta_receber_pagto aux
        	JOIN conta_receber_parcela crp ON crp.id = aux.conta_receber_parcela_id
        	JOIN conta_receber cr ON cr.id = crp.conta_receber_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'conta_receber_parcela' AS entity, count(aux.id) AS total
        FROM conta_receber_parcela aux
        	JOIN conta_receber cr ON cr.id = aux.conta_receber_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'conta_receber_parcela_evento' AS entity, count(aux.id) AS total
        FROM conta_receber_parcela_evento aux
        	JOIN conta_receber_parcela crp ON crp.id = aux.conta_receber_parcela_id
        	JOIN conta_receber cr ON cr.id = crp.conta_receber_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'domain' AS entity, count(id) AS total
        FROM domain
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY id
    UNION
        SELECT 'domain_address' AS entity, count(id) AS total
        FROM domain_address
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'domain_and_table_sequence' AS entity, count(id) AS total
        FROM domain_and_table_sequence
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'domain_contact' AS entity, count(id) AS total
        FROM domain_contact
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'domain_org' AS entity, count(id) AS total
        FROM domain_org
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY id
    UNION
        SELECT 'domain_sequence' AS entity, count(id) AS total
        FROM domain_sequence
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'equipe_venda' AS entity, count(id) AS total
        FROM equipe_venda
    UNION
        SELECT 'equipe_venda_catalogo' AS entity, count(aux.id) AS total
        FROM equipe_venda_catalogo aux
        	JOIN equipe_venda ev ON ev.id = aux.equipe_venda_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'erro_integracao' AS entity, count(id) AS total
        FROM erro_integracao
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'erro_integracao_externa' AS entity, count(aux.id) AS total
        FROM erro_integracao_externa aux
        	JOIN log_erro_integracao_externa leie ON leie.id = aux.log_erro_integracao_externa_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'fabricante' AS entity, count(aux.id) AS total
        FROM fabricante aux
        	JOIN parceiro p ON p.id = aux.id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'file_infosys' AS entity, count(id) AS total
        FROM file_infosys
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'forma_pagamento' AS entity, count(id) AS total
        FROM forma_pagamento
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'tarefa' AS entity, count(id) AS total
        FROM tarefa
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'tarefa_limite_credito_evento' AS entity, count(aux.id) AS total
        FROM tarefa_limite_credito_evento aux
        	JOIN tarefa f ON f.id = aux.tarefa_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'grupo' AS entity, count(id) AS total
        FROM grupo
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'image' AS entity, count(aux.id) AS total
        FROM image aux
        	JOIN file_infosys fi ON fi.id = aux.id
    UNION
        SELECT 'instituicao_pagamento' AS entity, count(aux.id) AS total
        FROM instituicao_pagamento aux
        	JOIN domain_org dorg ON dorg.id = aux.domain_org_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'justificativa' AS entity, count(id) AS total
        FROM justificativa
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'movimentacao_financeira' AS entity, count(id) AS total
        FROM movimentacao_financeira
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'movimentacao_financeira_evento' AS entity, count(aux.id) AS total
        FROM movimentacao_financeira_evento aux
        	JOIN movimentacao_financeira mf ON mf.id = aux.movimentacao_financeira_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'natureza_financeira' AS entity, count(id) AS total
        FROM natureza_financeira
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'natureza_operacao' AS entity, count(id) AS total
        FROM natureza_operacao
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce' AS entity, count(id) AS total
        FROM nfce
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_autxml' AS entity, count(aux.id) AS total
        FROM nfce_autxml aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_cana_deduc' AS entity, count(aux.id) AS total
        FROM nfce_cana_deduc aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_cana_fordia' AS entity, count(aux.id) AS total
        FROM nfce_cana_fordia aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_cobr_dup' AS entity, count(aux.id) AS total
        FROM nfce_cobr_dup aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_evento' AS entity, count(aux.id) AS total
        FROM nfce_evento aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_evento_sefaz' AS entity, count(aux.id) AS total
        FROM nfce_evento_sefaz aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_ide_nfref' AS entity, count(aux.id) AS total
        FROM nfce_ide_nfref aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_inconsistencia' AS entity, count(aux.id) AS total
        FROM nfce_inconsistencia aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_infadic_obscont' AS entity, count(aux.id) AS total
        FROM nfce_infadic_obscont aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_infadic_obsfisco' AS entity, count(aux.id) AS total
        FROM nfce_infadic_obsfisco aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_infadic_procref' AS entity, count(aux.id) AS total
        FROM nfce_infadic_procref aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_item' AS entity, count(aux.id) AS total
        FROM nfce_item aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_item_prod_arma' AS entity, count(aux2.id)
        FROM nfce_item_prod_arma aux2
        	JOIN nfce_item aux ON aux.id = aux2.nfce_item_id
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux2.created_at IS NOT NULL AND (aux2.created_at > \'{de}\' AND aux2.created_at < \'{ate}\'))
		    OR (aux2.updated_at IS NOT NULL AND (aux2.updated_at > \'{de}\' AND aux2.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_item_prod_detexport' AS entity, count(aux2.id)
        FROM nfce_item_prod_detexport aux2
        	JOIN nfce_item aux ON aux.id = aux2.nfce_item_id
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux2.created_at IS NOT NULL AND (aux2.created_at > \'{de}\' AND aux2.created_at < \'{ate}\'))
		    OR (aux2.updated_at IS NOT NULL AND (aux2.updated_at > \'{de}\' AND aux2.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_item_prod_di' AS entity, count(aux2.id)
        FROM nfce_item_prod_di aux2
        	JOIN nfce_item aux ON aux.id = aux2.nfce_item_id
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux2.created_at IS NOT NULL AND (aux2.created_at > \'{de}\' AND aux2.created_at < \'{ate}\'))
		    OR (aux2.updated_at IS NOT NULL AND (aux2.updated_at > \'{de}\' AND aux2.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_item_prod_di_adi' AS entity, count(aux3.id)
        FROM nfce_item_prod_di_adi aux3
        	JOIN nfce_item_prod_di aux2 ON aux2.id = aux3.nfce_item_prod_di_id
        	JOIN nfce_item aux ON aux.id = aux2.nfce_item_id
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux3.created_at IS NOT NULL AND (aux3.created_at > \'{de}\' AND aux3.created_at < \'{ate}\'))
		    OR (aux3.updated_at IS NOT NULL AND (aux3.updated_at > \'{de}\' AND aux3.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_item_prod_rastro' AS entity, count(aux2.id)
        FROM nfce_item_prod_rastro aux2
        	JOIN nfce_item aux ON aux.id = aux2.nfce_item_id
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux2.created_at IS NOT NULL AND (aux2.created_at > \'{de}\' AND aux2.created_at < \'{ate}\'))
		    OR (aux2.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux2.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_pag_detpag' AS entity, count(aux.id) AS total
        FROM nfce_pag_detpag aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_pedido' AS entity, count(aux.id) AS total
        FROM nfce_pedido aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_transp_reboque' AS entity, count(aux.id) AS total
        FROM nfce_transp_reboque aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfce_transp_vol' AS entity, count(aux.id) AS total
        FROM nfce_transp_vol aux
        	JOIN nfce n ON n.id = aux.nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe' AS entity, count(aux.id) AS total
        FROM nfe aux
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_autxml' AS entity, count(aux.id) AS total
        FROM nfe_autxml aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_cana_deduc' AS entity, count(aux.id) AS total
        FROM nfe_cana_deduc aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_cana_fordia' AS entity, count(aux.id) AS total
        FROM nfe_cana_fordia aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_cobr_dup' AS entity, count(aux.id) AS total
        FROM nfe_cobr_dup aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_evento' AS entity, count(aux.id) AS total
        FROM nfe_evento aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_evento_sefaz' AS entity, count(aux.id) AS total
        FROM nfe_evento_sefaz aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_ide_nfref' AS entity, count(aux.id) AS total
        FROM nfe_ide_nfref aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_inconsistencia' AS entity, count(aux.id) AS total
        FROM nfe_inconsistencia aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_infadic_obscont' AS entity, count(aux.id) AS total
        FROM nfe_infadic_obscont aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_infadic_obsfisco' AS entity, count(aux.id) AS total
        FROM nfe_infadic_obsfisco aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_infadic_procref' AS entity, count(aux.id) AS total
        FROM nfe_infadic_procref aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_item' AS entity, count(aux.id) AS total
        FROM nfe_item aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_item_prod_arma' AS entity, count(aux2.id)
        FROM nfe_item_prod_arma aux2
        	JOIN nfe_item aux ON aux.id = aux2.nfe_item_id
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux2.created_at IS NOT NULL AND (aux2.created_at > \'{de}\' AND aux2.created_at < \'{ate}\'))
		    OR (aux2.updated_at IS NOT NULL AND (aux2.updated_at > \'{de}\' AND aux2.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_item_prod_detexport' AS entity, count(aux2.id)
        FROM nfe_item_prod_detexport aux2
        	JOIN nfe_item aux ON aux.id = aux2.nfe_item_id
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux2.created_at IS NOT NULL AND (aux2.created_at > \'{de}\' AND aux2.created_at < \'{ate}\'))
		    OR (aux2.updated_at IS NOT NULL AND (aux2.updated_at > \'{de}\' AND aux2.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_item_prod_di' AS entity, count(aux2.id)
        FROM nfe_item_prod_di aux2
        	JOIN nfe_item aux ON aux.id = aux2.nfe_item_id
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux2.created_at IS NOT NULL AND (aux2.created_at > \'{de}\' AND aux2.created_at < \'{ate}\'))
		    OR (aux2.updated_at IS NOT NULL AND (aux2.updated_at > \'{de}\' AND aux2.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_item_prod_di_adi' AS entity, count(aux3.id)
        FROM nfe_item_prod_di_adi aux3
        	JOIN nfe_item_prod_di aux2 ON aux2.id = aux3.nfe_item_prod_di_id
        	JOIN nfe_item aux ON aux.id = aux2.nfe_item_id
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux3.created_at IS NOT NULL AND (aux3.created_at > \'{de}\' AND aux3.created_at < \'{ate}\'))
		    OR (aux3.updated_at IS NOT NULL AND (aux3.updated_at > \'{de}\' AND aux3.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_item_prod_rastro' AS entity, count(aux2.id)
        FROM nfe_item_prod_rastro aux2
        	JOIN nfe_item aux ON aux.id = aux2.nfe_item_id
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux2.created_at IS NOT NULL AND (aux2.created_at > \'{de}\' AND aux2.created_at < \'{ate}\'))
		    OR (aux2.updated_at IS NOT NULL AND (aux2.updated_at > \'{de}\' AND aux2.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_pag_detpag' AS entity, count(aux.id) AS total
        FROM nfe_pag_detpag aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_pedido' AS entity, count(aux.id) AS total
        FROM nfe_pedido aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_pedido_produto' AS entity, count(aux2.id)
        FROM nfe_pedido_produto aux2
        	JOIN nfe_pedido aux ON aux.id = aux2.nfe_pedido_id
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux2.created_at IS NOT NULL AND (aux2.created_at > \'{de}\' AND aux2.created_at < \'{ate}\'))
		    OR (aux2.updated_at IS NOT NULL AND (aux2.updated_at > \'{de}\' AND aux2.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_transp_reboque' AS entity, count(aux.id) AS total
        FROM nfe_transp_reboque aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'nfe_transp_vol' AS entity, count(aux.id) AS total
        FROM nfe_transp_vol aux
        	JOIN nfe n ON n.id = aux.nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'parceiro' AS entity, count(id) AS total
        FROM parceiro
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'parceiro_contato' AS entity, count(aux.id) AS total
        FROM parceiro_contato aux
        	JOIN parceiro p ON p.id = aux.parceiro_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'parceiro_endereco' AS entity, count(aux.id) AS total
        FROM parceiro_endereco aux
        	JOIN parceiro p ON p.id = aux.parceiro_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'pedido' AS entity, count(id) AS total
        FROM pedido
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'pedido_integracao' AS entity, count(id) AS total
        FROM pedido_integracao
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'pedido_integracao_evento' AS entity, count(aux.id) AS total
        FROM pedido_integracao_evento aux
        	JOIN pedido_integracao pint ON pint.id = aux.pedido_integracao_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'pedido_nfce' AS entity, count(id) AS total
        FROM pedido_nfce
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'pedido_nfce_evento' AS entity, count(aux.id) AS total
        FROM pedido_nfce_evento aux
        	JOIN pedido_nfce pn ON pn.id = aux.pedido_nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'pedido_nfce_forma_pagamento' AS entity, count(aux.id) AS total
        FROM pedido_nfce_forma_pagamento aux
        	JOIN pedido_nfce pn ON pn.id = aux.pedido_nfce_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'pedido_nfe' AS entity, count(id) AS total
        FROM pedido_nfe
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'pedido_nfe_evento' AS entity, count(aux.id) AS total
        FROM pedido_nfe_evento aux
        	JOIN pedido_nfe pn ON pn.id = aux.pedido_nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'pedido_nfe_forma_pagamento' AS entity, count(aux.id) AS total
        FROM pedido_nfe_forma_pagamento aux
        	JOIN pedido_nfe pn ON pn.id = aux.pedido_nfe_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'pedido_pre_pedido' AS entity, count(aux.id) AS total
        FROM pedido_pre_pedido aux
        	JOIN pedido p ON p.id = aux.pedido_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'pedido_produto' AS entity, count(aux.id) AS total
        FROM pedido_produto aux
        	JOIN pedido p ON p.id = aux.pedido_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'portador' AS entity, count(id) AS total
        FROM portador
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'portaria' AS entity, count(id) AS total
        FROM portaria
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'pre_cliente' AS entity, count(id) AS total
        FROM pre_cliente
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'pre_cliente_evento' AS entity, count(aux.id) AS total
        FROM pre_cliente_evento aux
        	JOIN pre_cliente pc ON pc.id = aux.pre_cliente_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'pre_pedido' AS entity, count(id) AS total
        FROM pre_pedido
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'pre_pedido_evento' AS entity, count(aux.id) AS total
        FROM pre_pedido_evento aux
        	JOIN pre_pedido pp ON pp.id = aux.pre_pedido_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'produto' AS entity, count(id) AS total
        FROM produto
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'produto_entrada_fiscal' AS entity, count(id) AS total
        FROM produto_entrada_fiscal
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'produto_entrada_fiscal_evento' AS entity, count(aux.id) AS total
        FROM produto_entrada_fiscal_evento aux
        	JOIN produto_entrada_fiscal pef ON pef.id = aux.produto_entrada_fiscal_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'produto_entrada_fiscal_produto_fiscal' AS entity, count(aux.id) AS total
        FROM produto_entrada_fiscal_produto_fiscal aux
        	JOIN produto_entrada_fiscal pef ON pef.id = aux.produto_entrada_fiscal_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'produto_estoque_evento' AS entity, count(aux.id) AS total
        FROM produto_estoque_evento aux
        	JOIN produto p ON p.id = aux.produto_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'produto_fiscal' AS entity, count(id) AS total
        FROM produto_fiscal
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'produto_fiscal_cbenef' AS entity, count(aux.id) AS total
        FROM produto_fiscal_cbenef aux
        	JOIN produto_fiscal pf ON pf.id = aux.produto_fiscal_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'produto_fiscal_regra_fiscal' AS entity, count(aux.id) AS total
        FROM produto_fiscal_regra_fiscal aux
        	JOIN produto_fiscal pf ON pf.id = aux.produto_fiscal_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'produto_fiscal_mva' AS entity, count(aux.id) AS total
        FROM produto_fiscal_mva aux
        	JOIN produto_fiscal pf ON pf.id = aux.produto_fiscal_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'produto_tarefa' AS entity, count(aux.id) AS total
        FROM produto_tarefa aux
        	JOIN produto p ON p.id = aux.produto_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'produto_imagem' AS entity, count(aux.id) AS total
        FROM produto_imagem aux
        	JOIN produto p ON p.id = aux.produto_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'produto_pre_entrada' AS entity, count(id) AS total
        FROM produto_pre_entrada
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'produto_pre_entrada_evento' AS entity, count(aux.id) AS total
        FROM produto_pre_entrada_evento aux
        	JOIN produto_pre_entrada ppe ON ppe.id = aux.produto_pre_entrada_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'produto_tabela_preco' AS entity, count(aux.id) AS total
        FROM produto_tabela_preco aux
        	JOIN produto p ON p.id = aux.produto_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'promocao_produto' AS entity, count(id) AS total
        FROM promocao_produto
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'promocao_produto_evento' AS entity, count(aux.id) AS total
        FROM promocao_produto_evento aux
        	JOIN promocao_produto pp ON pp.id = aux.promocao_produto_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'promocao_produto_produto' AS entity, count(aux.id) AS total
        FROM promocao_produto_produto aux
        	JOIN promocao_produto pp ON pp.id = aux.promocao_produto_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'ree' AS entity, count(id) AS total
        FROM ree
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'ree_evento' AS entity, count(aux.id) AS total
        FROM ree_evento aux
        	JOIN ree r ON r.id = aux.ree_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'ree_produto' AS entity, count(aux.id) AS total
        FROM ree_produto aux
        	JOIN ree r ON r.id = aux.ree_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'regra_fiscal' AS entity, count(id) AS total
        FROM regra_fiscal
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'rse' AS entity, count(id) AS total
        FROM rse
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'rse_evento' AS entity, count(aux.id) AS total
        FROM rse_evento aux
        	JOIN rse r ON r.id = aux.rse_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'rse_produto' AS entity, count(aux.id) AS total
        FROM rse_produto aux
        	JOIN rse r ON r.id = aux.rse_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'serie_fiscal' AS entity, count(id) AS total
        FROM serie_fiscal
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'supervisor' AS entity, count(aux.id) AS total
        FROM supervisor aux
        	JOIN parceiro p ON p.id = aux.id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'tabela_preco' AS entity, count(id) AS total
        FROM tabela_preco
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'tag' AS entity, count(id) AS total
        FROM tag
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'terminal' AS entity, count(id) AS total
        FROM terminal
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'terminal_operador' AS entity, count(aux.id) AS total
        FROM terminal_operador aux
        	JOIN terminal t ON t.id = aux.terminal_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'timeline_event' AS entity, count(id) AS total
        FROM timeline_event
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'timeline_event_user' AS entity, count(aux.id) AS total
        FROM timeline_event_user aux
        	JOIN timeline_event te ON te.id = aux.timeline_event_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'tipo_operacao' AS entity, count(id) AS total
        FROM tipo_operacao
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'token' AS entity, count(aux.id) AS total
        FROM "token" aux
			JOIN "user" u ON u.id = aux.user_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'uficms' AS entity, count(id) AS total
        FROM uficms
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
        GROUP BY domain_org_id
    UNION
        SELECT 'unidade' AS entity, count(id) AS total
        FROM unidade
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'user' AS entity, count(id) AS total
        FROM "user"
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'vendedor' AS entity, count(id) AS total
        FROM vendedor
        WHERE ((created_at IS NOT NULL AND (created_at > \'{de}\' AND created_at < \'{ate}\'))
		    OR (updated_at IS NOT NULL AND (updated_at > \'{de}\' AND updated_at < \'{ate}\')))
    UNION
        SELECT 'vendedor_cliente' AS entity, count(aux.id) AS total
        FROM vendedor_cliente aux
        	JOIN vendedor v ON v.id = aux.vendedor_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
    UNION
        SELECT 'vendedor_perde_ganha_evento' AS entity, count(aux.id) AS total
        FROM vendedor_perde_ganha_evento aux
        	JOIN vendedor v ON v.id = aux.vendedor_id
        WHERE ((aux.created_at IS NOT NULL AND (aux.created_at > \'{de}\' AND aux.created_at < \'{ate}\'))
		    OR (aux.updated_at IS NOT NULL AND (aux.updated_at > \'{de}\' AND aux.updated_at < \'{ate}\')))
) AS query
ORDER BY query.entity;
"""  # noqa