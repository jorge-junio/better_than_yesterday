# Banco único

A aplicação usa o backend PostgreSQL padrão do Django e apenas o schema `public`. O domínio não seleciona mais um tenant. Os hosts ainda precisam estar em `ALLOWED_HOSTS`.

## Instalação nova

Configure `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` e `DB_PORT` para um banco vazio e execute:

```sh
python manage.py migrate --noinput
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

O Docker executa `migrate` na inicialização. A importação de vocabulário agora é direta:

```sh
python manage.py import_english_words_from_csv
```

Os comandos `setup_tenants`, `tenant_command` e `setup_superuser --schema` foram removidos. Para criação não interativa do administrador, use `createsuperuser --noinput`, com `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL` e `DJANGO_SUPERUSER_PASSWORD` no ambiente.

## Transferir os dados existentes

Não basta executar `migrate` sobre o banco antigo: os dados de `jjsistemas` continuam no schema antigo e não passam automaticamente para `public`. Use um banco novo para preservar o original e permitir retorno à versão anterior.

1. Pare as gravações na aplicação antiga durante a exportação e mantenha-as interrompidas até a troca. Faça um backup completo com `pg_dump`, usando as credenciais do ambiente antigo:

   ```sh
   pg_dump -Fc -h HOST -p PORT -U USUARIO -d BANCO_ANTIGO -f backup-antes-banco-unico.dump
   ```

2. **Ainda na versão antiga**, com `django-tenants` instalado e o banco antigo configurado, exporte o tenant escolhido:

   ```sh
   python manage.py tenant_command dumpdata --schema=jjsistemas --all --natural-foreign --natural-primary --exclude=tenants --exclude=contenttypes --exclude=auth.permission --exclude=sessions --indent=2 --output=dados-jjsistemas.json
   ```

   O arquivo contém usuários, hashes de senhas, grupos, vínculos às permissões e dados dos módulos. Trate-o como dado privado. Tipos de conteúdo e permissões padrão serão recriados por `migrate`; sessões não serão transferidas, exigindo novo login. Permissões cadastradas manualmente, se existirem, precisam ser recriadas antes da importação.

3. Crie um banco PostgreSQL vazio, configure a nova versão para esse banco e importe antes de liberar o acesso:

   ```sh
   python manage.py migrate --noinput
   python manage.py loaddata dados-jjsistemas.json
   python manage.py check
   python manage.py collectstatic --noinput
   ```

   Não crie usuários nem cadastros no destino antes de carregar o arquivo. O superusuário existente será importado com sua senha atual. Copie também o diretório de mídia, caso existam arquivos enviados.

4. Confira login, permissões, totais de registros e os fluxos de tarefas, avaliações, treinos e compras. Só então aponte a aplicação para o banco novo e libere o acesso. Guarde o banco antigo e o backup até validar a transferência.

Esse procedimento transfere um tenant. Dados de vários tenants não devem ser carregados juntos sem um plano de conciliação de IDs e cadastros. Para retornar à versão anterior, restaure também sua configuração de banco e dependências; alterações feitas no banco novo após a troca não existirão no antigo.
