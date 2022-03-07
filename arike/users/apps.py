from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "arike.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import arike.users.signals  # noqa F401
            import care.models.signals
        except ImportError:
            pass
