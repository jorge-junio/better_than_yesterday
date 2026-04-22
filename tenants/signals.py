
# descobrir como rodar isso só depois que o schema for criado


# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from django_tenants.utils import schema_context
# from .models import Client

# @receiver(post_save, sender=Client)
# def create_tenant_superuser(sender, instance, created, **kwargs):
#     # Só agimos na criação de um novo registro e ignoramos o schema 'public'
#     if created and instance.schema_name not in ['public', 'jjsistemas']:
#         User = get_user_model()

#         # 'instance.schema_name' é o nome do schema que acabou de ser criado
#         with schema_context(instance.schema_name):
#             # Criamos o superusuário dentro do contexto deste cliente
#             User.objects.create_superuser(
#                 username='admin',
#                 email=f'admin@{instance.schema_name}.com',
#                 password='senha_padrao_123'
#             )
#             print(f"✅ Superusuário criado para o tenant: {instance.schema_name}")
