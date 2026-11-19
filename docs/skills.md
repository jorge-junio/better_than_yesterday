# Skills individuais por tarefa

## Uso

Abra Nova missão ou Edite uma tarefa e selecione **Skill desenvolvida**. As opções são Inteligência, Força, Disciplina, Sabedoria e Carisma. Sem skill continua sendo uma opção válida; a categoria não interfere na escolha.

Exemplos: leitura e cursos podem receber Inteligência; uma tarefa de exercício físico pode receber Força. Essa escolha é feita pelo usuário, sem classificação automática.

As barras ficam em **Personagem** e **Evolução**. A skill também aparece nos cards de missão/dashboard, na agenda e no detalhe da tarefa.

## Pontos e ciclo de vida

- 15 XP gerais por tarefa concluída, conforme a regra existente.
- Se houver uma skill, a mesma conclusão contribui com 15 XP para ela; o XP geral permanece 15, e não 30.
- 100 XP por nível; nível inicial 1.
- XP calculado a partir das tarefas com `completed_at` preenchido. Não há um contador de pontos para incrementar, duplicar ou dessincronizar.
- Reenvio de conclusão: mesma tarefa, mesmos 15 XP.
- Reabertura ou exclusão: a contribuição deixa de existir, assim como já ocorre no XP geral.
- Mudança de skill em tarefa concluída: retira 15 XP da anterior e atribui à nova. Isso também permite classificar manualmente tarefas antigas.
- Sem skill: contribui somente para a evolução geral.

O campo fica em `Task`, que alimenta a agenda e as missões. Nas tarefas recorrentes geradas, a escolha pode ser feita por ocorrência. Não foi introduzida recompensa automática para sessões de treino, avaliações ou tarefas de projeto, nem um vínculo automático com categorias.

O escopo de consulta acompanha o XP geral existente, que é calculado sobre as tarefas da aplicação. Não foram introduzidos proprietários, contadores ou novas regras de isolamento neste incremento.

## Implementação

- `tasks/models.py`: enum das cinco skills e campo opcional `skill`.
- `tasks/migrations/0012_task_skill.py`: adição do campo; padrão vazio para preservar os registros existentes. Migração aplicada ao banco de trabalho após validação em banco descartável; não havia outras migrações pendentes.
- `tasks/forms.py`: seletor de skill e sincronização de `is_completed`/`completed_at` ao salvar pelo formulário. Marcar Concluída no formulário agora usa a mesma fonte de verdade das ações rápidas; não basta salvar apenas o booleano.
- `tasks/services.py`: `get_skill_progress`, com uma agregação por skill. Nenhuma alteração nos contadores gerais ou serviços de treino/compras.
- `app/views.py` e `progress/views.py`: contexto de skills para Personagem e Evolução.
- `app/templates/life_rpg/skill_progress.html`: componente de progresso reutilizado nas duas telas.
- Templates de missão, agenda, dashboard e detalhe: identificação da skill escolhida.
- `static/app/screens.css`: cards de skills e identificação nos cards de missão.

## Validação

- 91 testes existentes passaram.
- Três cenários de integração temporários em PostgreSQL descartável passaram: ciclo concluir/reabrir/ignorar/excluir/trocar skill; níveis e validação do formulário; cadastro/edição via HTTP e renderização das telas.
- Conferido que duas conclusões da mesma tarefa somam somente 15 XP; 120 XP produzem nível 2, progresso 20/100 e faltam 80 XP; skill inválida é rejeitada; reabertura pelo formulário remove os pontos.
- Migração criada e aplicada com sucesso. `manage.py check`, `makemigrations --check --dry-run` e `git diff --check` passaram.
- Chrome em 320, 390, 430 e 1280 px: cinco cards de skills, valores corretos de progresso e ausência de overflow horizontal. Prévia mobile inspecionada visualmente.
- Testes adicionais e prévias ficaram em `/tmp`. Não foram criados arquivos de teste no repositório nem tarefas de demonstração no banco de trabalho.
