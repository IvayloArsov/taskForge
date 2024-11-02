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
        on_delete=models.CASCADE,
        related_name='projects_created'
    )
    members = models.ManyToManyField(
        User,
        related_name='projects_member_of'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    lead_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='projects_lead'
    )

    def __str__(self):
        return self.name
