from django.apps import AppConfig


class GestioAprendicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.gestionAprendices'
    
    def ready(self):
        import applications.gestionAprendices.signals.documentos_signals
