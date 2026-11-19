# Dashboard — primeira etapa Life RPG

Registro histórico da primeira etapa. Para a migração das demais telas e o estado atual do shell compartilhado, consulte `docs/interface_life_rpg.md`.

Implementação de `docs/refatoracao_interface.md` limitada à tela `/dashboard/`.

## Estrutura entregue

- Shell próprio em HTML, CSS e JavaScript nativos, sem Bootstrap, bibliotecas de ícones, HTMX ou Chart.js carregados nessa tela.
- Cabeçalho contextual, personagem, experiência, nível, sequência, três indicadores diários, cards de missões, ação de criação e relatórios de evolução.
- Avatar existente de `assetcs/avatars/chibi.png`, copiado para `static/app/avatars/chibi.png` e enquadrado por CSS. O original foi preservado. O contêiner `data-avatar` admite estados; `celebrating` usa animação CSS curta com suporte a movimento reduzido.
- Navegação inferior: Início, Missões, Personagem, Evolução e Perfil. Personagem e Evolução apontam para seções reais do dashboard nesta etapa. Missões usa a tela existente e sua permissão de consulta.
- Perfil em `dialog` nativo com saída e acesso às áreas existentes. Escape, foco modal, retorno de foco e bloqueio da rolagem ao fundo.

## Arquivos

Criados:

- `static/app/life-rpg.css`: tokens da paleta, layout, componentes, responsividade e animações.
- `static/app/life-rpg.js`: painel de perfil, gráficos DOM, navegação, feedback e atualização automática.
- `static/app/avatars/chibi.png`: cópia publicável do avatar fornecido.
- `app/templates/life_rpg/icon.html`: componente SVG reutilizável.
- `docs/dashboard_interface.md`: este registro.

Modificados nesta etapa:

- `progress/templates/progress/dashboard.html`: shell independente.
- `progress/templates/progress/partials/dashboard_content.html`: componentes do dashboard.
- `progress/views.py`: contexto de gamificação existente e saudação; entrada via HTMX legado solicita navegação completa para o shell novo.
- `tasks/views.py`: conclusão do dia aceita `return_to=dashboard`, de destino fixo. Chamadas anteriores mantêm seus retornos.

## Funcionalidades e regras preservadas

- `get_today_mission_context` continua sendo a fonte do nível, XP, patente e sequência. Recompensa existente: 15 XP por conclusão; 100 XP por nível. Não foi criado modelo de classe, atributo ou recompensa.
- O serviço existente também mantém a geração de recorrências do dia, como na tela atual de missões.
- Conclusões usam o serviço existente, POST com CSRF, permissão `tasks.change_task` e a data da missão. Sem mudança no banco ou nas regras de conclusão.
- Criação e detalhes continuam usando as rotas existentes; botões respeitam permissões.
- Período customizado, validação de datas, contagens de hoje/período, distribuição por status, produtividade por dia da semana e lista de pendências foram mantidos. Os gráficos usam DOM/progress nativos.
- Atualização a cada 60 segundos verifica mudanças e recarrega os dados quando necessário, preservando a posição de rolagem. Não interrompe filtros editados, formulários em foco ou perfil aberto. Falhas de conexão conservam a tela atual.
- Áreas Inglês, Tarefas, Projetos, Treinos e Compras continuam acessíveis pelo painel Perfil. As demais telas mantêm a interface anterior até sua etapa de refatoração.

## Validação

- `manage.py check`: sem problemas.
- `manage.py test progress`: cinco testes existentes passaram; nenhum arquivo de teste foi criado no repositório.
- `node --check static/app/life-rpg.js` e `git diff --check`: passaram.
- Verificações temporárias fora do repositório, com serviços simulados: renderização sem dependências de interface, estado vazio/zero XP, filtros inválidos, entrada HTMX, sessão anônima, permissão de conclusão e retorno dashboard/legado.
- Chrome headless com HTML renderizado e dados simulados: 320×740, 360×800, 390×844, 430×932, 768×1024, 1280×900 e 844×390. Sem overflow horizontal; navegação inferior fixa; avatar/gráficos carregados; controles da navegação com pelo menos 44×44 px.
- Perfil: foco dentro do modal, fechamento com Escape e retorno ao acionador. Movimento reduzido e ausência de exceções JavaScript verificados. Prévia de 390 px inspecionada visualmente.
- As verificações de fluxo usaram mocks e não gravaram dados nem criaram usuários no banco. Fluxo completo com uma conta real permanece para validação de uso.

## Próximas etapas

- Refatorar a tela de missões e seus formulários, incluindo criação/edição em bottom sheet.
- Desenvolver as telas independentes de Personagem, Evolução e Perfil quando sua etapa for iniciada, mantendo os acessos existentes durante a transição.
- Refatorar as demais áreas e remover as dependências legadas conforme cada tela for migrada. Esta etapa não anuncia remoção global dessas dependências.
