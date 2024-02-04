from django.apps import AppConfig


class AuthUserConfig(AppConfig):
    verbose_name = 'Пользователи'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_user'
