from django.apps import AppConfig


class AgendarcitasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.agendarcitas'

    def ready(self):
        import applications.agendarcitas.signals  # Asegúrate de importar las señales