from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    # overwrite the ready method: this method is called, when this app is ready(initialized)
    def ready(self) -> None:
        import store.signals.handlers
