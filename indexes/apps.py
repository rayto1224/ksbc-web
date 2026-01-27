# indexes/apps.py
from django.apps import AppConfig


class IndexesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "indexes"
    verbose_name = "HomePage Mgt"  # 在后台显示的中文名
