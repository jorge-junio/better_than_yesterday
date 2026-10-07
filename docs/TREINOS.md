# Uso do módulo de treinos

O grupo **Treinos** contém **Treino**, **Histórico** e **Treinar**.
Cada usuário administra sua programação e seus resultados dentro do tenant atual.

## Primeiro treino

1. Em **Treino**, escolha **Novo treino**, informe nome e data inicial e marque **Ativo**. A data final é opcional; deixe em branco enquanto o treino não tiver um encerramento definido.
2. Abra a programação e adicione os exercícios aos dias da semana, indicando ordem, séries e repetições.
3. Selecione um exercício já cadastrado ou informe um novo nome. O mesmo exercício pode ser usado em vários dias e treinos.
4. Em **Treinar**, escolha a programação do dia e toque em **Iniciar treino**.
5. Após cada série, informe as repetições e o peso em kg e toque em **Registrar série**. A confirmação **Salvo** indica que o servidor gravou o resultado.
6. Use **Atualizar série** para corrigir um registro durante a sessão.
7. Finalize o treino. Séries pendentes exigem confirmação e produzem uma sessão parcial.

Use 0 kg quando não houver carga externa. O peso informado pode ter duas casas decimais.
Escolher a programação de outro dia não muda a data real da sessão.

## Descanso entre séries

No cadastro ou edição do treino, defina **Descanso entre séries (segundos)**. O padrão é 60 segundos; use 0 para desativar, até o limite de 3.600 segundos. Novas sessões usam esse valor, preservado mesmo após editar o treino.

Após registrar uma nova série com sucesso, um contador aparece na tela. Você pode pular o descanso. Ao chegar a zero, ele mostra **Descanso concluído**. Atualizações de séries e falhas ao salvar não reiniciam o contador. A contagem acompanha o horário de término, inclusive ao alternar de aplicativo, e pode ser retomada ao recarregar a sessão na mesma aba.

## Copiar um dia

Na programação do treino, use **Copiar dia** no card de um dia com exercícios. Selecione outro dia da semana e confirme em **Copiar exercícios**. Os exercícios serão acrescentados ao final do destino, preservando os que já estavam lá. A origem e o histórico não mudam. Os exercícios copiados podem ser editados individualmente depois.

## Retomada e histórico

- Uma sessão em andamento pode ser retomada em **Treinar** ou no **Histórico**.
- A programação original da sessão é preservada, mesmo após editar ou arquivar o treino.
- O histórico finalizado é somente leitura.
- Arquivar desativa o treino. Restaurar não o ativa automaticamente.
- O acompanhamento exige internet. Em falhas, os campos continuam preenchidos para tentar novamente; mudanças não registradas não sobrevivem ao fechamento da página.

## Relatórios

Os filtros do histórico também controlam os relatórios, que usam todos os resultados encontrados, além da página atual.
A taxa de séries compara os registros com as séries previstas nas sessões selecionadas.
Selecione um exercício para ver gráficos e tabela de evolução nas últimas 30 sessões com registros.
O volume é a soma de peso × repetições, conforme a carga informada pelo usuário.

## Instalação e permissões

O app `workouts` está em `TENANT_APPS`. Aplique as migrações em cada ambiente:

```sh
python manage.py migrate_schemas --noinput
python manage.py check
```

Superusuários têm acesso automático. Para contas comuns, atribua no administrador as permissões adequadas:

- **Treino**: consultar, adicionar e alterar treino; arquivamento usa a permissão de alteração.
- **Programação**: adicionar, alterar e excluir exercício do treino.
- **Histórico e Treinar**: consultar sessão de treino.
- **Iniciar sessão**: adicionar sessão de treino.
- **Registrar séries, marcar exercícios e finalizar**: alterar sessão de treino.

As permissões não dão acesso aos treinos de outros usuários pela aplicação.
