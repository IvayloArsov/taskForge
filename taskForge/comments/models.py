from django.contrib.auth import get_user_model
from django.db import models

from taskForge.tickets.models import Ticket

User = get_user_model()

class Comment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author.first_name} {self.author.last_name}'