# Product Requirements Document (PRD) - Sistema de Controle de Tarefas

## 1. Visão Geral
O objetivo deste sistema é fornecer uma plataforma centralizada para gestão de produtividade pessoal ou de equipe. O diferencial reside na automação de tarefas recorrentes que alimentam uma agenda diária dinâmica, permitindo que o usuário foque na execução sem perder tempo com cadastros repetitivos.

## 2. Personas
- **Usuário Organizador:** Precisa de uma visão clara do que deve ser feito hoje e quer automatizar rotinas semanais ou mensais.
- **Gestor de Resultados:** Utiliza o dashboard para analisar a consistência e conclusão de tarefas ao longo do tempo.

## 3. Requisitos Funcionais

### 3.1. Gestão de Tarefas Recorrentes
O sistema deve permitir a configuração de regras para geração automática de tarefas.
- **RF01 - Recorrência por Dias da Semana:** O usuário seleciona dias específicos (ex: Seg, Qua, Sex) para a tarefa aparecer na agenda.
- **RF02 - Recorrência por Range de Datas:** O usuário define um período de início e fim (ex: de 10 a 20 de cada mês ou um intervalo fixo no ano).
- **RF03 - Recorrência por Datas Específicas:** O usuário marca datas isoladas no calendário para que a tarefa seja gerada.
- **RF04 - Edição de Modelo:** Alterar uma tarefa recorrente deve dar a opção de atualizar apenas as futuras ou as já geradas na agenda (que não foram concluídas).

### 3.2. Agenda do Dia (Interface Principal)
- **RF05 - Consolidação de Tarefas:** A agenda deve exibir, ao carregar o dia, todas as tarefas geradas pela recorrência + tarefas criadas manualmente para aquela data.
- **RF06 - Visualização Padrão:** A tela principal deve listar inicialmente apenas as tarefas **não concluídas**.
- **RF07 - Filtro de Status:** Deve haver um toggle ou filtro para exibir as tarefas já concluídas.
- **RF08 - Ações Rápidas:** Marcar como concluída, editar horário, excluir ou adiar tarefa.

### 3.3. Dashboard e Relatórios
- **RF09 - Visão de Hoje:** Exibição gráfica do percentual de conclusão das tarefas do dia atual.
- **RF10 - Range de Datas Customizado:** Permitir que o usuário selecione um intervalo (Início - Fim) para visualizar:
    - Total de tarefas criadas vs. concluídas.
    - Taxa de produtividade por dia da semana.
    - Listagem de tarefas pendentes no período.

## 4. Requisitos Não Funcionais
- **RNF01 - Performance:** A geração de tarefas recorrentes para a agenda não deve causar lentidão no carregamento da tela principal.
- **RNF02 - Persistência:** Uma tarefa gerada por recorrência, uma vez concluída, deve manter seu estado mesmo se a regra de recorrência original for alterada.
- **RNF03 - Interface Responsiva:** O sistema deve ser acessível via desktop e dispositivos móveis.

## 5. Fluxo de Usuário (User Flow)
1. O usuário acessa o menu **"Recorrências"** e cadastra "Academia" para Segundas e Quartas.
2. O sistema verifica a data atual. Se for uma Segunda-feira, ao abrir a **"Agenda do Dia"**, a tarefa "Academia" já estará listada.
3. O usuário adiciona manualmente "Comprar Pão" na agenda de hoje.
4. O usuário conclui "Academia". A tela principal agora mostra apenas "Comprar Pão".
5. O usuário ativa o filtro "Ver concluídas" e ambas aparecem na lista.
6. O usuário acessa o **"Dashboard"**, seleciona os últimos 7 dias e vê o gráfico de sua evolução.

## 6. Critérios de Aceite
- O sistema deve gerar a tarefa na agenda às 00:00 do dia previsto.
- Tarefas manuais não devem se repetir a menos que sejam convertidas em recorrentes.
- O dashboard deve calcular corretamente as métricas mesmo em períodos que cruzem meses diferentes.

## 7. Treinos e acompanhamento físico

### 7.1. Navegação e escopo
- Grupo **Treinos**, com itens **Treino**, **Histórico** e **Treinar**.
- Dados isolados por usuário dentro do tenant. As permissões Django controlam cadastro, consulta e execução.
- Interface em português, com campos numéricos, cartões e botões adequados ao celular.

### 7.2. Programação
- Nome, data inicial, data final opcional e indicador de ativo. Quando informada, a data final deve ser igual ou posterior à inicial. Sem data final, o treino permanece válido a partir da data inicial, enquanto estiver ativo.
- Descanso entre séries configurado em segundos no treino: padrão de 60, limite de 3.600 e 0 para desativar. O valor é copiado para cada nova sessão.
- Apenas um treino ativo por usuário, protegido também no banco. Substituir o ativo exige confirmação.
- Cards de dias com exercícios começam minimizados e podem ser expandidos e minimizados individualmente, mantendo visíveis o dia e a ação de adicionar exercício.
- Exercícios reutilizáveis por usuário, organizados por dia da semana, ordem, séries, repetições previstas por série e observações opcionais.
- Copiar a programação de um dia para outro no mesmo treino, preservando exercícios, séries, repetições, observações e ordem relativa. A cópia é acrescentada ao final do destino, sem alterar a origem ou o histórico. Não permitir copiar para o mesmo dia ou modificar treino arquivado.
- Séries e repetições previstas são positivas. Limites por exercício: 100 séries e 1.000 repetições por série.
- Arquivar desativa o treino, mas preserva o histórico; restaurar o mantém inativo.

### 7.3. Execução
- Selecionar a programação semanal (padrão: dia atual) e iniciar uma sessão na data atual, usando o fuso do sistema.
- Novas sessões exigem treino ativo dentro da validade e exercícios no dia escolhido.
- Apenas uma sessão em andamento por usuário. Reabrir Treinar permite retomar a sessão, mesmo se o treino original for alterado ou arquivado.
- Cada sessão copia nome do treino, nomes dos exercícios, metas, ordem e observações. Alterações na programação não modificam esses registros.
- Cada série salva repetições realizadas e peso em kg, com até duas casas decimais. Zero é permitido, inclusive para carga externa inexistente.
- Registrar série grava imediatamente; atualizar série corrige o mesmo registro durante a sessão. Envios repetidos não duplicam séries ou sessões.
- Iniciar uma contagem regressiva visível após a primeira gravação bem-sucedida de cada série; correções, reenvios e falhas não iniciam nem reiniciam o descanso. Permitir pular o descanso e mostrar sua conclusão. Preservar a contagem ao recarregar ou retomar a sessão na mesma aba, usando o horário de término para evitar atraso ao deixar a página em segundo plano.
- Exibir estados de gravação e erros, preservar campos em falhas de conexão e avisar antes de sair com alterações não registradas. A primeira versão exige internet.
- Marcar um exercício sem séries registradas como não realizado; permitir retomá-lo.
- Finalizar sem pendências resulta em sessão concluída; pendências exigem confirmação e resultam em sessão parcial. Histórico finalizado é somente leitura.

### 7.4. Histórico e relatórios
- Histórico disponível desde o início, com situação, data, programação usada e detalhe por série.
- Filtros por período, treino, exercício e situação.
- Relatórios sobre todos os resultados filtrados, independentemente da paginação: sessões concluídas por semana/mês (últimos 12 períodos com resultados), séries registradas versus previstas e resultados por exercício.
- Evolução por exercício nas últimas 30 sessões registradas: maior carga, repetições totais, séries e volume (soma de kg × repetições), com gráficos e tabela.
- Mostrar a última execução registrada do exercício como referência durante o treino.

### 7.5. Aceite
- Isolamento entre usuários e tenants em todas as consultas e alterações.
- Restrição de único treino ativo e única sessão aberta, inclusive com requisições concorrentes.
- Retomada dos dados salvos após fechar a página, sem duplicações ao reenviar.
- Mudanças e remoções na programação não alteram sessões existentes.
- Séries inválidas e tentativas de alterar sessões encerradas são rejeitadas.
- Validar fluxo completo, relatórios, permissões e layout de celular sem criar arquivos de teste no repositório.

## 8. Revisão de avaliações de vocabulário

- Exibir um item respondido por vez nos detalhes da avaliação, com posição atual e navegação anterior/próximo.
- Manter o resumo com os totais da avaliação inteira.
- Salvar a posição na URL para que editar uma palavra, salvar, cancelar ou recarregar retorne ao mesmo item.
- Oferecer a navegação também no celular e no carregamento parcial via HTMX.

## 9. Compras e feira

- Grupo **Compras**, com **Itens da feira**, **Fazer feira** e **Histórico**, com ícones compatíveis com a interface.
- Listas reutilizáveis por usuário dentro do tenant, com nome, criação automática e situação ativa/inativa. Várias listas podem estar ativas.
- Cada lista tem seus próprios itens com nome e situação ativa/inativa, sem nomes duplicados na mesma lista (ignorando maiúsculas/minúsculas).
- Escolher uma lista ativa e pré-selecionar pelo menos um dos seus itens ativos antes de iniciar a compra.
- Uma compra em andamento por usuário, com possibilidade de retomar ou cancelar mediante confirmação.
- Cada compra copia o nome da lista e dos itens selecionados. Alterações no cadastro não mudam compras iniciadas nem o histórico.
- Informar quantidades decimais não negativas (até três casas decimais), com opção de salvar o progresso. Zero indica item não comprado.
- Finalização exige quantidade informada para todos os itens, ao menos um item com quantidade positiva e valor total em reais não negativo com até duas casas decimais. Confirmar o total encerra a compra e torna seus dados somente para consulta.
- Histórico com data, situação, nome da lista, itens, quantidades e valor total. Filtrar por período de finalização e somar o gasto das compras concluídas em todo o período filtrado.
- Permissões Django e isolamento por usuário em todas as consultas e gravações; proteção contra criação duplicada e finalização repetida. Layout adequado ao celular e fluxo completo validado sem arquivos de teste no repositório.
