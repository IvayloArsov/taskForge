from email.policy import default

from django.contrib.auth import get_user_model
from django.db import models

from taskForge.projects.models import Project
from taskForge.tickets.choices import TicketPriority, TicketStatus

User = get_user_model()


# Create your models here.
class BaseTicket(models.Model):
    title = models.CharField(
        max_length=200,
    )
    description = models.TextField()
    priority = models.CharField(
        max_length=30,
        choices=TicketPriority,
        default=TicketPriority.MEDIUM
    )
    status = models.CharField(
        max_length=30,
        choices=TicketStatus,
        default=TicketStatus.OPEN
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='%(class)ss'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_%(class)ss'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_%(class)ss'
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        help_text="Expected completion date"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract=True
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Ticket(BaseTicket):
    is_bug_ticket = models.BooleanField(default=False)
    original_bug_report = models.OneToOneField(
        'BugReport',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='converted_ticket'
    )


class BugReport(BaseTicket):
    is_approved = models.BooleanField(default=False)