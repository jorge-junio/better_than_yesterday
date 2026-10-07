# Compras e feira

## Cadastro

No menu **Compras → Itens da feira**, crie uma lista com nome e situação ativa. A data de criação é registrada automaticamente. Abra **Ver itens** para adicionar ou editar os nomes dos itens e indicar se estão ativos.

Você pode manter várias listas ativas. Itens e listas inativos continuam no cadastro, mas não aparecem para iniciar novas compras. A mesma lista não aceita itens com nomes duplicados, ignorando diferenças entre maiúsculas e minúsculas.

## Fazer feira

1. Abra **Compras → Fazer feira** e selecione uma lista ativa.
2. Marque os itens que pretende comprar e clique em **Iniciar compras**.
3. Informe a quantidade de cada item. Decimais são permitidos, como `1,5`, com até três casas decimais. Use `0` para um item que não foi comprado.
4. Use **Salvar progresso** durante a feira. As quantidades são gravadas ao salvar; antes de sair com alterações pendentes, o navegador solicita confirmação.
5. Ao retornar a **Fazer feira**, clique em **Continuar compras** para retomar a compra em andamento. Só há uma compra em andamento por usuário.
6. Clique em **Finalizar compras**, confira as quantidades, informe o valor total em reais e clique em **Confirmar compra**.

Finalizar exige quantidade preenchida em todos os itens e pelo menos um item com quantidade positiva. O total aceita zero e valores com até duas casas decimais, por exemplo `150,90`. Uma compra iniciada por engano pode ser encerrada em **Cancelar compra**, mediante confirmação.

## Histórico

O histórico permite consultar compras concluídas e canceladas, filtrar pela data de encerramento e ver os itens e as quantidades. O total do período soma somente compras concluídas e considera todas as páginas dos resultados.

Compras concluídas ficam somente para consulta. Cada compra preserva os nomes da lista e dos itens no momento de início; alterações posteriores no cadastro não mudam o histórico.

## Operação

O módulo exige conexão com o servidor. Os dados pertencem ao usuário dentro de cada tenant. As permissões Django de `shopping` controlam visualização, cadastro e execução; conceda as permissões aos grupos desejados em **Admin → Grupos**. Superusuários já possuem acesso.

Na implantação, execute `python manage.py migrate` e `python manage.py collectstatic --noinput` no ambiente configurado do servidor.
