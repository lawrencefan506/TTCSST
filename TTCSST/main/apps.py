from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"

    def ready(self):
        from scripts import updater
        if not hasattr(updater, '_scheduler_started') or not updater._scheduler_started:
            updater.start()
            updater._scheduler_started = True
