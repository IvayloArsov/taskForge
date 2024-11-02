from django.db import models


class UserRoleChoices(models.TextChoices):
    ADMIN = 'admin', 'Administrator'
    MANAGER = 'manager', 'Project Manager'
    DEVELOPER = 'dev', 'Developer'
    END_USER = 'end_user', 'End User'
