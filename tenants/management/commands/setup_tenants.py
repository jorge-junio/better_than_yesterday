from django.core.management.base import BaseCommand
from django.utils import timezone
from tenants.models import Client, Domain

class Command(BaseCommand):
    help = 'Cria o tenant público inicial e um tenant de teste para a arquitetura multi-tenant'

    def handle(self, *args, **options):
        # Captura o momento exato da execução
        agora = timezone.now()

        self.stdout.write(self.style.NOTICE('Iniciando setup de tenants...'))

        # 1. Criando o esquema público
        if not Client.objects.filter(schema_name='public').exists():
            tenant_publico = Client(
                schema_name='public', 
                name='Gestão Principal', 
                paid_until='2099-12-31', 
                on_trial=False
            )
            tenant_publico.save()
            Domain.objects.create(
                domain='demonstracaolocal.com', 
                tenant=tenant_publico, 
                is_primary=True
            )
            self.stdout.write(self.style.SUCCESS('Tenant public criado com sucesso.'))
        else:
            self.stdout.write('Tenant public já existe.')

        # 2. Criando o primeiro cliente de teste
        schema_name = 'jjsistemas'
        if not Client.objects.filter(schema_name=schema_name).exists():
            # Exemplo: Criando com validade de 30 dias a partir de hoje
            data_validade = agora + timezone.timedelta(days=30)
            
            client = Client(
                schema_name=schema_name, 
                name='JJ Sistemas', 
                paid_until=data_validade, 
                on_trial=True
            )
            client.save() # O django-tenants dispara a criação do schema no Postgres aqui
            Domain.objects.create(
                domain='jjsistemas.demonstracaolocal.com', 
                tenant=client, 
                is_primary=True
            )
            self.stdout.write(self.style.SUCCESS(f'Cliente "{schema_name}" criado com sucesso.'))
        else:
            self.stdout.write(f'Cliente "{schema_name}" já existe.')
