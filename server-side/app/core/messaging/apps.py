from django.apps import AppConfig

class MessagingConfig(AppConfig):
    name = 'core.messaging'

    def ready(self):
        import core.messaging.signals  # Ensure signals are imported
