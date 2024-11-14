from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from taskForge.projects.models import Project
from django.core.cache import cache

from taskForge.tickets.models import Ticket, BugReport


@receiver(post_save, sender=Project)
def ensure_project_lead_is_member_on_save(sender, instance, created, **kwargs):
    """
    Adds the project's lead to the list of members
    if the lead isn't selected during the creation of the project
    """
    if instance.lead_by and instance.lead_by not in instance.members.all():
        instance.members.add(instance.lead_by)


@receiver(m2m_changed, sender=Project.members.through)
def ensure_project_lead_stays_member(sender, instance, action, pk_set, **kwargs):
    """
    Prevents the removal of the project's lead from the members list
    """
    if action == "pre_remove" and instance.lead_by and instance.lead_by.pk in pk_set:
        pk_set.remove(instance.lead_by.pk)


def invalidate_project_cache(project_id):
    cache.delete(f'team_workload_project_{project_id}')
    cache.delete(f'project_stats_{project_id}')


@receiver([post_save, post_delete], sender=Ticket)
def clear_cache_on_ticket_change(sender, instance, **kwargs):
    invalidate_project_cache(instance.project_id)


@receiver([post_save, post_delete], sender=BugReport)
def clear_cache_on_bug_change(sender, instance, **kwargs):
    invalidate_project_cache(instance.project_id)
