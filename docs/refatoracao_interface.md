# Refatoração da interface — Life RPG

## 1. Objetivo

Analise o projeto existente e refatore sua interface para transformá-lo em um aplicativo web mobile-first de produtividade gamificada, inspirado em RPGs, com um avatar chibi estilo anime.

O resultado deve parecer um aplicativo mobile nativo, mesmo sendo executado diretamente no navegador.

**Requisito obrigatório:** toda a interface deve ser implementada exclusivamente com HTML5, CSS3 e JavaScript puro (Vanilla JavaScript).

Não utilize React, Vue, Angular, Svelte, jQuery, Tailwind, Bootstrap, bibliotecas de componentes, frameworks CSS ou bibliotecas de animação.

Antes de modificar qualquer arquivo, examine a estrutura atual do projeto, identifique as funcionalidades existentes e preserve seu funcionamento.

## 2. Direção visual

Utilize uma identidade visual minimalista, moderna e elegante, combinando elementos de aplicativos de produtividade com características sutis de jogos RPG.

Características:

- Tema escuro como padrão.
- Superfícies com diferentes níveis de contraste.
- Bordas arredondadas e discretas.
- Espaçamento consistente.
- Tipografia moderna, com excelente legibilidade.
- Ícones minimalistas.
- Animações suaves e rápidas.
- Interface limpa, evitando excesso de elementos decorativos.
- Destaques em roxo e lavanda.
- Elementos de gamificação integrados naturalmente à interface.

### Paleta de cores

Defina variáveis CSS globais:

```css
:root {
  color-scheme: dark;

  --bg-primary: #10131e;
  --bg-secondary: #1c2232;
  --bg-tertiary: #272e40;

  --accent-primary: #a78bfa;
  --accent-secondary: #c4b5fd;

  --text-primary: #f8fafc;
  --text-secondary: #aab0c0;
  --text-muted: #737d91;

  --border-color: #343b4f;

  --success: #86efac;
  --warning: #fbbf24;
  --danger: #fb7185;

  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;

  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
}
```

Centralize as configurações visuais nessas variáveis para facilitar futuras personalizações.

## 3. Layout principal

Crie uma estrutura de aplicativo mobile com:

### App Shell

- Área principal ocupando toda a altura disponível.
- Cabeçalho compacto.
- Conteúdo central com rolagem vertical.
- Navegação inferior fixa.
- Respeito às safe areas do dispositivo.
- Nenhuma rolagem horizontal indesejada.
- Layout adaptável a diferentes tamanhos de tela.

Utilize `100dvh` quando apropriado, com fallback para navegadores antigos.

### Bottom Navigation

Implemente uma barra inferior com cinco destinos:

1. Início
2. Missões
3. Personagem
4. Evolução
5. Perfil

A barra deve apresentar:

- Ícones SVG simples.
- Identificação textual.
- Destaque visual do item ativo.
- Áreas de toque com pelo menos 44 × 44 pixels.
- Suporte à navegação por teclado.
- Transições discretas.

Não utilize bibliotecas de ícones. Utilize SVGs locais ou inline.

## 4. Tela inicial — Dashboard

A tela inicial deve ser a principal experiência do aplicativo.

Organize os elementos nesta ordem:

### 4.1 Cabeçalho

Exiba uma saudação contextual, como:

"Boa tarde, aventureiro!"

Inclua a data atual e um botão de configurações ou perfil.

### 4.2 Card do personagem

Crie um card visualmente destacado contendo:

- Avatar chibi.
- Nome do personagem.
- Classe atual.
- Nível.
- Barra de experiência.
- XP atual e XP necessário para o próximo nível.
- Indicador de sequência de dias ativos.

O avatar deve ocupar uma posição de destaque sem prejudicar a visualização das informações.

Utilize o avatar chibi fornecido como referência visual.

Se houver um arquivo de imagem do avatar no projeto, reutilize-o. Caso contrário, crie uma estrutura preparada para receber esse arquivo posteriormente.

Não substitua o personagem por emojis ou imagens aleatórias.

### 4.3 Resumo diário

Apresente três indicadores:

- Missões concluídas.
- XP conquistado hoje.
- Progresso diário percentual.

Utilize cards compactos.

### 4.4 Missões do dia

Apresente as missões em cards contendo:

- Nome da tarefa.
- Categoria ou atributo relacionado.
- Quantidade de XP.
- Indicador de conclusão.
- Ícone da categoria.

As missões concluídas devem receber tratamento visual diferenciado.

Inclua um botão para visualizar todas as missões.

### 4.5 Ação principal

Disponibilize um botão destacado para adicionar uma nova missão.

Utilize um Floating Action Button ou botão equivalente, evitando sobreposição com a navegação inferior.

## 5. Tela de missões

Implemente uma interface de gerenciamento de tarefas com:

- Abas para tarefas diárias, semanais e hábitos, conforme os tipos suportados pelo projeto.
- Lista de missões.
- Filtros de status.
- Indicadores de dificuldade.
- Recompensas em XP.
- Botão de criação.
- Estados vazios.
- Feedback visual ao concluir uma tarefa.

Utilize cards com hierarquia visual clara.

### Criação e edição

Utilize um Bottom Sheet para criar ou editar missões.

O painel deve:

- Abrir a partir da parte inferior.
- Possuir animação suave.
- Permitir fechamento por botão.
- Permitir fechamento pela tecla Escape.
- Gerenciar corretamente o foco.
- Bloquear a interação com o conteúdo ao fundo enquanto estiver aberto.
- Respeitar as safe areas.
- Ajustar-se ao teclado virtual.

Não introduza novas regras de negócio sem necessidade.

## 6. Tela do personagem

Esta tela deve apresentar o avatar chibi em destaque.

Inclua áreas para:

- Visualização do personagem.
- Nome.
- Classe.
- Nível.
- Experiência.
- Atributos.
- Conquistas.
- Personalização visual futura.

### Avatar

O avatar deve ser renderizado com uma estrutura reutilizável.

Prepare o CSS e JavaScript para suportar futuramente:

- Diferentes expressões.
- Roupas.
- Acessórios.
- Poses.
- Estados de animação.

Não implemente um motor de avatar complexo nesta etapa.

A estrutura deve permitir substituir a imagem principal ou trabalhar futuramente com camadas PNG transparentes.

### Reações

Prepare estados visuais como:

- idle
- happy
- celebrating
- thinking

Quando uma missão for concluída, o avatar poderá apresentar uma animação curta de comemoração.

Utilize animações CSS com `transform` e `opacity`, respeitando `prefers-reduced-motion`.

## 7. Tela de evolução

Apresente os atributos do personagem com barras de progresso.

Atributos iniciais sugeridos:

- Força
- Inteligência
- Disciplina
- Sabedoria
- Carisma

Cada atributo deve apresentar:

- Nome.
- Ícone.
- Nível.
- Experiência acumulada.
- Progresso até o próximo nível.

Se o projeto já possuir atributos próprios, preserve-os em vez de substituí-los.

Prepare uma área para futura árvore de habilidades, mas não implemente funcionalidades fictícias.

## 8. Tela de perfil

Organize configurações e informações gerais:

- Informações do usuário.
- Preferências visuais.
- Configurações do aplicativo.
- Exportação de dados, se já existente.
- Importação de dados, se já existente.
- Informações sobre o aplicativo.

Não remova funcionalidades presentes no projeto original.

## 9. Componentes reutilizáveis

Implemente componentes reutilizáveis utilizando funções JavaScript e elementos DOM nativos.

Componentes desejados:

- AppHeader
- BottomNavigation
- AvatarCard
- ExperienceBar
- StatCard
- QuestCard
- AttributeBar
- BottomSheet
- Modal
- Toast
- ProgressRing
- EmptyState
- FloatingActionButton

Os nomes são sugestões de organização, não exigem arquitetura específica.

Evite duplicação de HTML e CSS.

Utilize templates HTML ou funções de criação de elementos quando apropriado.

Não introduza um sistema complexo de componentes caso a estrutura atual não necessite.

## 10. Interações e animações

Implemente animações CSS leves:

- Entrada de cards.
- Transições entre estados.
- Preenchimento de barras de XP.
- Feedback de conclusão.
- Pequeno movimento de comemoração do avatar.
- Abertura e fechamento de Bottom Sheets.
- Destaque do item selecionado na navegação.

Prefira propriedades eficientes como `transform` e `opacity`.

Evite animações excessivas ou contínuas que possam prejudicar o desempenho em smartphones.

Respeite as preferências de acessibilidade do sistema.

## 11. Responsividade

Priorize telas de smartphones entre 320 e 430 pixels de largura, sem limitar o funcionamento a essas dimensões.

Em telas maiores:

- Centralize o conteúdo principal.
- Utilize largura máxima adequada.
- Preserve a experiência de aplicativo.
- Evite esticar cards excessivamente.
- Adapte a navegação quando necessário.

A interface deve funcionar em orientação vertical e horizontal.

## 12. Acessibilidade

Garanta:

- HTML semântico.
- Contraste adequado.
- Labels em controles.
- Navegação por teclado.
- Indicadores de foco visíveis.
- Feedback acessível para mudanças de estado.
- Suporte a leitores de tela.
- Botões com tamanho adequado para toque.
- Preferência por movimento reduzido.

Utilize elementos nativos sempre que possível.

## 13. Arquitetura CSS e JavaScript

Respeite a arquitetura atual do projeto.

Se for necessário reorganizar os arquivos, utilize uma estrutura semelhante a:

```text
src/
  index.html
  assets/
    avatars/
    icons/
  css/
    variables.css
    reset.css
    layout.css
    components.css
    screens.css
    animations.css
  js/
    app.js
    components/
    screens/
    services/
    utils/
```

Esta estrutura é apenas uma referência.

Não reorganize o projeto inteiro se isso não trouxer benefícios concretos.

Utilize módulos ES nativos quando apropriado.

Não adicione dependências externas.

## 14. Preservação das funcionalidades

Esta é uma exigência crítica.

Antes da refatoração:

1. Identifique todas as telas existentes.
2. Identifique os fluxos de navegação.
3. Identifique as funcionalidades implementadas.
4. Identifique a persistência de dados.
5. Identifique os eventos e regras de negócio.

Durante a refatoração:

- Preserve funcionalidades existentes.
- Preserve contratos de dados.
- Preserve regras de XP e evolução, se já implementadas.
- Preserve os mecanismos de persistência.
- Evite alterações desnecessárias no backend.
- Não apague dados existentes.
- Não substitua funcionalidades reais por demonstrações estáticas.
- Não introduza dados fictícios no fluxo de produção.

Se alguma alteração funcional for inevitável, explique o motivo.

## 15. Critérios de aceitação

Considere a tarefa concluída somente quando:

- A interface estiver visualmente consistente.
- A experiência for mobile-first.
- O avatar estiver integrado ao layout.
- A navegação funcionar.
- As missões existentes continuarem operacionais.
- As barras de progresso refletirem dados reais.
- Os componentes forem reutilizáveis.
- Não houver frameworks ou bibliotecas de interface.
- Não houver dependências externas adicionadas.
- O layout não apresentar overflow horizontal.
- Os controles forem acessíveis.
- O projeto continuar executando normalmente.

## 16. Processo de execução

Execute o trabalho nesta sequência:

**Etapa 1 — Inspeção**

Analise a estrutura do projeto e identifique os arquivos relevantes.

**Etapa 2 — Planejamento**

Defina quais arquivos serão modificados, quais componentes serão criados e como preservar as funcionalidades existentes.

**Etapa 3 — Implementação**

Implemente a nova interface diretamente no projeto, seguindo os requisitos acima.

**Etapa 4 — Validação**

Execute as verificações disponíveis no projeto. Se houver ambiente de testes ou navegador automatizado disponível, valide também os fluxos principais e a responsividade.

**Etapa 5 — Relatório**

Ao finalizar, apresente:

- Arquivos criados.
- Arquivos modificados.
- Componentes implementados.
- Funcionalidades preservadas.
- Testes realizados.
- Pendências identificadas.

Não se limite a apresentar sugestões ou exemplos isolados: implemente a refatoração no código existente.

**Resultado esperado:** um aplicativo web de produtividade gamificada, com visual minimalista premium, avatar chibi estilo anime e experiência de uso semelhante a um aplicativo Android nativo, utilizando exclusivamente HTML, CSS e JavaScript puro.