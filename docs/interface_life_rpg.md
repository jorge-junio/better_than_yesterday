# Interface Life RPG — migração das telas restantes

Implementação de `docs/refatoracao_interface.md` após a primeira etapa do dashboard.

## Cobertura

A interface de produto agora compartilha tema escuro, tokens roxo/lavanda, superfícies, tipografia, formulários, cards, feedback, SVGs locais e navegação inferior fixa. Nenhuma tela de produto carrega Bootstrap, fonte de ícones, HTMX ou Chart.js. O Django Admin mantém a interface administrativa própria do Django.

Áreas migradas:

- Login.
- Dashboard e seus relatórios.
- Missões do dia, agenda, detalhes, cadastro, edição, exclusão e ações rápidas.
- Categorias e tarefas recorrentes, incluindo seleção de dias e datas.
- Projetos, tarefas de projeto e possíveis tarefas, com seus formulários, detalhes e ações existentes.
- Vocabulário: palavras, significados, observações, importação e exportação.
- Avaliações: cadastro, edição, quiz, resumo e revisão paginada com retorno ao item.
- Treinos: programação, exercícios, cópia de dia, execução, registro de séries, descanso, finalização, histórico e gráficos.
- Compras: listas, itens, seleção, compra em andamento, quantidades, finalização, cancelamento e histórico.
- Menus das seções.
- Novas páginas independentes de Personagem (`/character/`), Evolução (`/evolution/`) e Perfil (`/profile/`).

## Componentes e arquitetura

- `base.html` usa os estilos locais `life-rpg.css` e `screens.css`; os nomes de classes de layout já usados nos templates foram preservados com regras locais próprias para reduzir mudanças nos formulários e no domínio. Não foi incluído framework CSS.
- `life_rpg/navigation.html` apresenta Início, Missões, Personagem, Evolução e Perfil. O Perfil mantém acesso a todas as áreas autorizadas e ao logout por POST/CSRF.
- `life_rpg/icon.html` centraliza SVGs inline, sem dependência de fonte ou CDN.
- `life_rpg/avatar_card.html` reutiliza o avatar e os números reais no Dashboard e no Personagem. Personagem mostra nível, patente, XP, sequência e selos do serviço já existente. Nenhum atributo ou habilidade fictícia foi introduzido.
- `progress/partials/evolution_content.html` compartilha os filtros e relatórios entre Dashboard e Evolução.
- `interface.js` implementa painel inferior de missões, foco, Escape, feedback, inicialização de campos, significados, recorrências, expansão de dias e salvamento local dos componentes que precisam continuar na tela.
- Criação/edição de tarefas, recorrências e tarefas de projeto abre em `dialog` nativo a partir dos links; acesso direto também usa o painel. Sem JavaScript, as mesmas URLs e formulários continuam acessíveis como páginas.
- Links e formulários comuns usam navegação HTTP nativa. Séries de treino e quantidades de compras usam Fetch, FormData e o contrato de fragmentos existente no servidor. Os cabeçalhos HTTP `HX-Request`, `HX-Redirect` e `HX-Trigger-After-Swap` foram mantidos como compatibilidade do servidor, sem carregar ou reproduzir a biblioteca HTMX.
- `workouts.js` mantém controle de alterações, descanso baseado em horário final e armazenamento por sessão na aba. Os gráficos de evolução foram substituídos por SVGs construídos com DOM nativo, com os mesmos dados e tabela de resultados.
- O contador fica acima da navegação inferior, sem sobreposição. Painéis têm rolagem própria, limites em `dvh`, safe areas e viewport configurado para redimensionamento pelo teclado quando suportado.
- Movimento reduzido, foco visível, labels, mensagens de estado e controles de toque permanecem disponíveis.

## Arquivos

Criados nesta etapa:

- `static/app/screens.css`.
- `static/app/interface.js`.
- `app/templates/life_rpg/navigation.html`.
- `app/templates/life_rpg/avatar_card.html`.
- `app/templates/life_rpg/character.html`.
- `app/templates/life_rpg/profile.html`.
- `progress/templates/progress/evolution.html`.
- `progress/templates/progress/partials/evolution_content.html`.
- `docs/interface_life_rpg.md`.

Principais arquivos modificados:

- `app/templates/base.html`, componentes de cabeçalho/rodapé/navegação e templates de login/menu.
- `app/navigation.py`, `app/urls.py` e `app/views.py`.
- Templates de `tasks`, `categories`, `recurring_tasks`, `projects`, `project_tasks`, `possible_tasks`, `english_words`, `evaluations`, `workouts` e `shopping`: navegação nativa, SVGs locais e estilos consistentes, preservando campos/rotas.
- `progress/views.py`, `progress/urls.py` e templates do dashboard.
- `tasks/views.py`: filtros visuais de status no dia, retorno ao dashboard e feedback de conclusão.
- `static/app/life-rpg.js`, `static/app/login.css`, `static/workouts/workouts.js`, `static/workouts/workouts.css` e `static/shopping/shopping.js`.
- `evaluations/tests.py`: corrigido o contexto da fixture de revisão para fornecer `items_page`, que o template e a view já exigiam. Não houve alteração de regras para satisfazer o teste.

## Preservação funcional

Não foram alterados modelos, migrations, regras de XP, classes de evolução, recorrências, permissões, snapshots/histórico, idempotência de registros, filtros ou formatos de exportação/importação. As telas novas consomem os serviços e dados existentes.

A tela de missões permite visualizar pendentes, concluídas, ignoradas ou todas usando os estados já existentes. O período e a categoria continuam disponíveis. Os fluxos de avaliações preservam a posição na URL; a navegação deixou de depender de carregamento parcial para funcionar.

Falhas de rede durante gravação de séries ou quantidades conservam valores, exibem erro e permitem reenvio. Novas gravações de série iniciam descanso apenas quando o servidor informa a primeira gravação; correções/reenvios/validações não reiniciam a contagem.

## Verificação realizada

- 124 templates compilados sem erros.
- 91 testes existentes passaram.
- `manage.py check`, `makemigrations --check --dry-run`, verificações de sintaxe dos quatro scripts e `git diff --check` passaram.
- Coleta e geração de manifest de estáticos validadas em diretório temporário; a pasta `staticfiles` existente não foi sobrescrita nesta etapa.
- Integração temporária com PostgreSQL: banco exclusivo `test_bty_ui_<identificador>`, criado/migrado/removido pelo runner do Django. Nenhum usuário ou dado de validação foi criado no banco de trabalho.
- 74 telas autenticadas renderizadas, mais login e finalização de compras: 76 páginas no conjunto de revisão visual.
- Fluxos reais no banco descartável: criação de missão, validação inválida, conclusão, estados de missão, primeira gravação/reenvio/erro de série, disparo único de descanso, gravação de quantidades, validação, finalização de feira, exportações, resposta de quiz, sessão e permissões. CSRF sem token negado; com token válido, formulário validado. Consultas de treinos/compras de outro usuário retornaram 404.
- Chrome headless: 76 páginas em 320, 430 e 1280 px, sem overflow horizontal, exceções JS ou falhas no avatar; navegação fixa. Páginas de amostra inspecionadas visualmente.
- Componentes no navegador: abertura do painel de missão, foco, Escape e retorno de foco; significados dinâmicos; seleção de dias; expansão de treino; gravação da série/progresso/descanso; gravação da compra em andamento.
- Verificações adicionais em 320/430/1280 px: painéis de recorrência e tarefa de projeto, gráficos SVG com dados reais do banco descartável, textos longos e movimento reduzido.
- Simulação de perda de conexão no navegador: repetições/peso e quantidades preservados, botões reabilitados e erros apresentados; nenhuma contagem de descanso iniciada por falha.
- Scripts e cenários adicionais ficaram em `/tmp`, sem novos arquivos de teste no repositório. As prévias do navegador foram HTMLs renderizados no banco descartável, servidos localmente; não representam dados de produção.

## Limites e continuidade

- A migração visual não criou regras de atributos, árvore de habilidades ou preferências persistentes. O incremento posterior de skills individuais está documentado em `docs/skills.md`; a interface continua apresentando dados reais.
- Não foi introduzida funcionalidade offline. A interface conserva os valores em falhas, mas a gravação continua exigindo conexão, conforme o PRD.
- O processo de publicação deve executar a coleta de estáticos já prevista no projeto. Os artefatos coletados preexistentes foram preservados para não misturar mudanças anteriores do usuário com esta etapa.
- O registro `docs/dashboard_interface.md` descreve a primeira etapa; o shell, a navegação e as páginas independentes foram unificados por esta migração.

## Ajuste de descoberta das áreas

Após feedback de uso, as áreas deixaram de depender do acesso pelo Perfil:

- Cabeçalho compartilhado com botão textual **Áreas** e menu nativo com todas as opções autorizadas, incluindo Palavras, Avaliações, Treino, Histórico e Treinar.
- Dashboard com atalhos visíveis para Inglês, Tarefas, Projetos, Treinos e Compras, conforme permissões.
- O Perfil mantém os acessos anteriores. Nenhuma rota foi removida.
- Menu conferido com permissões completas, parciais e sem permissões; Chrome em 320, 360, 390, 430 e 1280 px, sem overflow, com Escape e retorno de foco.

## Navegação de Áreas e Perfil — organização atual

- O ícone superior direito abre um menu nativo com exatamente duas opções: **Perfil** (`/profile/`) e **Sair** (POST para `/logout/`, protegido por CSRF).
- O menu inferior substitui Perfil por **Áreas**, com acesso a `/areas/`.
- A tela Áreas apresenta os destinos em cartões quadrados, agrupados nas seções autorizadas: Inglês, Tarefas, Projetos, Treinos e Compras. Cada quadrado abre diretamente a opção correspondente. Não há opção de área no cabeçalho.
- O Perfil concentra as informações da conta e mantém os recursos de dados existentes. Atalhos de áreas do dashboard continuam disponíveis.
- Menu de perfil fecha ao clicar fora ou usar Escape, devolvendo foco ao acionador. Foram preservados navegação por teclado e alvos de toque.
- Validação em PostgreSQL descartável: rota privada, 14 opções para acesso completo, estado vazio sem permissões, negação de áreas protegidas e logout real com sessão/CSRF (GET negado; POST sem token negado; POST com token encerra a sessão).
- Chrome em 320, 390, 430 e 1280 px: quadrados sem overflow, barra inferior fixa, duas opções do perfil, Escape/foco e fechamento externo. Nenhum dado de validação foi criado no banco de trabalho.

## Identidade visual atualizada

- O novo `staticfiles/chibi.png` fornecido pelo usuário foi copiado, sem alterações na imagem, para `static/app/avatars/chibi.png`, que é a fonte usada pela aplicação e preservada pela coleta de estáticos. O enquadramento CSS passou a centralizar a imagem inteira, pois o novo arquivo tem um único personagem central.
- `staticfiles/icon.png` foi copiado para `static/app/icon.png`. É usado na marca do cabeçalho/login, no favicon e no apple-touch-icon.
- `app_metadata.html` centraliza metadados no layout compartilhado e no login. `static/app/manifest.webmanifest` referencia o ícone fornecido para atalhos compatíveis, com nome Life RPG e cores atuais. Não foi introduzido suporte offline ou service worker.
- Arquivos fornecidos em `staticfiles` não foram removidos nem sobrescritos. Para futuras atualizações da aplicação, as fontes publicáveis são `static/app/icon.png` e `static/app/avatars/chibi.png`.
- Validação: cópias idênticas por hash, resolução pelos finders do Django, metadados no login/personagem, manifest válido e coleta de estáticos em diretório temporário. Personagem e nova marca inspecionados no Chrome em 390 px.

## Início focado nas missões do dia

O dashboard mantém saudação/data, três cards de resumo diário e missões. As seções de personagem, áreas e relatórios de evolução foram retiradas do Início; continuam disponíveis nas opções correspondentes da navegação.

Cada missão pendente no Início tem Concluir e um botão com ícone de cancelar para marcar **Não realizada neste dia**. A ação reutiliza `skip_task_for_today`, com POST/CSRF, permissão de alteração e data da tarefa, retornando ao dashboard. Não exclui a tarefa nem concede XP. Após o registro, a tarefa deixa de aparecer no Início; permanece disponível na agenda. O filtro de canceladas é aplicado antes do limite de cards, preservando espaço para as demais tarefas. Os dois controles ficam desabilitados durante o envio para evitar ações concorrentes pela interface.

Validação: 16 testes existentes de tarefas passaram. Cenário adicional em PostgreSQL descartável confirmou estado/retorno ao dashboard, ausência de XP na skill, tarefa preservada, reenvio sem mudança do registro original, retorno legado e negação sem permissão.

## Todas as missões do dia

O link **Ver todas** do Início abre `/tasks/today/all/`, uma tela dedicada às missões de hoje, com o mesmo resumo diário e o mesmo componente de card do dashboard, sem o limite de seis tarefas. Na tela completa, pendentes aparecem primeiro; concluídas e canceladas ficam em grupos recolhidos por padrão, cada um com a quantidade de itens no cabeçalho. Tarefas de outras datas não entram na listagem. No Início, canceladas continuam ocultas.

Os cards e o resumo foram extraídos para `tasks/partials/daily_quest_card.html` e `life_rpg/daily_summary.html`, evitando divergências de aparência ou ações entre as telas. Concluir e cancelar preservam a nova tela como destino; os destinos de retorno são restritos a nomes de rotas permitidos. O fluxo existente de agenda/filtros em `/tasks/today/` continua disponível.

Validação: 21 testes existentes de tarefas/progresso passaram; integração em PostgreSQL descartável confirmou seis cards no Início versus nove na listagem completa, exclusão de canceladas/outras datas, ações com retorno à tela correta e controle de acesso. Chrome em 320, 390, 430 e 1280 px confirmou nove cards, sem overflow horizontal nem erros de JavaScript.


A listagem completa foi verificada novamente com dez tarefas de hoje: oito pendentes, uma concluída e uma cancelada. Após concluir e cancelar mais uma, os grupos passaram a seis pendentes, duas concluídas e duas canceladas, sem duplicação e preservando o filtro do Início. Chrome em 320, 390, 430 e 1280 px confirmou os contadores, o estado recolhido inicial e a expansão dos dois grupos sem overflow.

## Filtro de categoria nas missões diárias

Início e `/tasks/today/all/` compartilham um filtro GET com opções Todas as categorias, Sem categoria e as categorias presentes nas tarefas de hoje. Resumo diário, listagens e contadores de concluídas/canceladas refletem a categoria escolhida; nível e XP total do personagem mantêm suas regras gerais.

`tasks/presentation.py` aplica a seleção validada por `DailyCategoryFilterForm` às duas telas, antes do limite de seis cards no Início. Uma categoria inválida exibe erro com lista vazia, sem erro de servidor. O componente `daily_category_filter.html` preserva o valor selecionado e oferece Limpar.

O link Ver todas, o botão Voltar e os POSTs de concluir/cancelar levam a seleção pela query string ou campo oculto. A atualização automática não interrompe o filtro enquanto ele é editado.

Verificações: 21 testes existentes de tarefas/progresso passaram. Integração temporária em PostgreSQL confirmou categorias distintas, Sem categoria, ausência de filtro, valores inválidos, contadores/resumo, limite do Início e retornos de concluir/cancelar mantendo a seleção. Chrome em 320, 390, 430 e 1280 px nas duas telas: categoria preservada, sem overflow horizontal nem erros JS. Nenhum dado de validação foi criado no banco de trabalho.

## Filtros expansíveis padronizados

Os filtros restantes seguem o painel nativo de `/tasks/today/`: cabeçalho **Filtros**, recolhido por padrão, expansão por clique/teclado e indicação de abrir/fechar. A alteração alcança Início, todas as missões de hoje, agenda, projetos, tarefas de projeto, possíveis tarefas, Evolução e históricos de treinos/compras. Os painéis já existentes nas missões e recorrências foram preservados.

Valores selecionados, parâmetros GET, botões de filtrar/limpar, resultados e paginação permanecem disponíveis. Quando há erro de validação, o painel abre para mostrar os campos a corrigir. A seleção da lista para iniciar uma feira permanece visível, pois prepara uma compra em vez de filtrar resultados.

O formulário de período da Evolução foi corrigido para enviar a `/evolution/#evolution`, permanecendo na própria tela; antes enviava ao dashboard, onde os relatórios já haviam sido removidos.

Verificação: 133 templates compilados, 91 testes existentes passaram, check do Django e diff sem erros. Nove telas renderizadas com formulários de filtro reais, sem consulta ao banco; confirmado que GET/action/valores e estado inicial foram preservados, inclusive abertura em erro de validação. Chrome em 320, 390 e 1280 px nas nove telas: recolhimento/expansão funcionando, sem overflow horizontal nem erros JS. Nenhum arquivo de teste foi criado no repositório.
