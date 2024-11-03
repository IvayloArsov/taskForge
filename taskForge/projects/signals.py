from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from taskForge.projects.models import Project

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
