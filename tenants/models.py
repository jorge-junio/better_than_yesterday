from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    # O campo 'schema_name' já vem no TenantMixin
    paid_until = models.DateField()
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    # Define se o schema deve ser criado automaticamente ao salvar o model
    auto_create_schema = True

class Domain(DomainMixin):
    # Relaciona o domínio (ex: cliente1.seuapp.com) ao schema
    pass