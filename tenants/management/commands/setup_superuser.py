import os
from django.core.management import call_command
from django.core.management.base import BaseCommand
from tenants.models import Client

class Command(BaseCommand):
    help = 'Cria um superusuário dentro de um schema específico de forma não interativa'

    def add_arguments(self, parser):
        parser.add_argument('--schema', type=str, required=True, help='O nome do schema (ex: cliente1)')
        parser.add_argument('--username', type=str, default='admin', help='Username do superusuário')
        parser.add_argument('--email', type=str, default='admin@exemplo.com', help='Email do superusuário')
        parser.add_argument('--password', type=str, default='Senha123@', help='Senha do superusuário')

    def handle(self, *args, **options):
        schema = options['schema']
        username = options['username']
        email = options['email']
        password = options['password']

        # Verifica se o tenant existe
        if not Client.objects.filter(schema_name=schema).exists():
            self.stdout.write(self.style.ERROR(f'Erro: O schema "{schema}" não existe.'))
            return

        try:
            self.stdout.write(self.style.NOTICE(f'Criando superusuário para o tenant: {schema}...'))

            # O tenant_command espera: 
            # 1. O nome do comando interno ('createsuperuser')
            # 2. O argumento --schema
            # 3. Os argumentos específicos do comando interno como strings formatadas
            
            call_command(
                'tenant_command',
                'createsuperuser',
                # Passamos as flags do createsuperuser como argumentos extras
                '--noinput',
                f'--username={username}',
                f'--email={email}',
                schema=schema,
            )
            
            # Como o createsuperuser no modo não-interativo não aceita senha via argumento no Django antigo,
            # usamos o modelo do Tenant para buscar o usuário recém criado e setar a senha.
            from django.contrib.auth import get_user_model
            from django_tenants.utils import schema_context

            with schema_context(schema):
                User = get_user_model()
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()

            self.stdout.write(self.style.SUCCESS(f'Sucesso! Superusuário "{username}" criado no schema "{schema}".'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Falha ao criar superusuário: {e}'))