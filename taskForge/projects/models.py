from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
    name = models.CharField(
        max_length=255,
    )
    description = models.TextField()
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_projects'
    )
    members = models.ManyToManyField(
        User,
        related_name='projects'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    lead_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='led_projects'
    )

    def __str__(self):
        return self.name