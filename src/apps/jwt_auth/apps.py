from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.jwt_auth"

    def ready(self):
        import apps.jwt_auth.schema  # noqa
