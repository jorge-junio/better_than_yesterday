from django.apps import AppConfig


class TenantsConfig(AppConfig):
    name = 'tenants'

    def ready(self):
        # Importante: Importar aqui para registrar os receivers
        import tenants.signals
