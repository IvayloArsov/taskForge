# taskForge/projects/apps.py
from django.apps import AppConfig

class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'taskForge.projects'

    def ready(self):
        import taskForge.projects.signals