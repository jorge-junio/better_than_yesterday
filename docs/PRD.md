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
