from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Profile, User
from ..projects.models import Project
from ..tickets.models import Ticket, BugReport


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, '_saving_profile'):
        try:
            instance._saving_profile = True
            if not hasattr(instance, 'profile'):
                Profile.objects.create(user=instance)
            instance.profile.save()
        finally:
            delattr(instance, '_saving_profile')

@receiver(post_save, sender=Profile)
def update_user_permissions(sender, instance, **kwargs):
    if hasattr(instance, '_updating_permissions'):
        return

    try:
        instance._updating_permissions = True
        user = instance.user

        user.groups.clear()

        if instance.role == 'manager':
            manager_group, created = Group.objects.get_or_create(name='Project Managers')

            if created:
                project_content_type=  ContentType.objects.get_for_model(Project)
                ticket_content_type = ContentType.objects.get_for_model(Ticket)
                bug_content_type = ContentType.objects.get_for_model(BugReport)

                manager_permissions = [
                    Permission.objects.get(content_type=project_content_type, codename='add_project'),
                    Permission.objects.get(content_type=project_content_type, codename='change_project'),
                    Permission.objects.get(content_type=project_content_type, codename='view_project'),

                    Permission.objects.get(content_type=ticket_content_type, codename='add_ticket'),
                    Permission.objects.get(content_type=ticket_content_type, codename='change_ticket'),
                    Permission.objects.get(content_type=ticket_content_type, codename='view_ticket'),

                    Permission.objects.get(content_type=bug_content_type, codename='add_bugreport'),
                    Permission.objects.get(content_type=bug_content_type, codename='change_bugreport'),
                    Permission.objects.get(content_type=bug_content_type, codename='view_bugreport'),
                ]
                manager_group.permissions.set(manager_permissions)

            user.groups.add(manager_group)
            if not user.is_staff:
                user.is_staff = True
                user.save(update_fields=['is_staff'])
        elif user.is_staff and not user.is_superuser:
            user.is_staff = False
            user.save(update_fields=['is_staff'])

    finally:
        delattr(instance, '_updating_permissions')