from django.apps import AppConfig


class A05AdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'a05_admin'
    # 这里可以自定义 子app 的名字
    verbose_name = "app_05_admin(change in apps.py)"
