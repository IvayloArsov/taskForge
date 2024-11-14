from django.utils import timezone

from django.db.models import Count
from django.core.cache import cache

from taskForge.accounts.choices import UserRoleChoices

CACHE_TIMEOUT = 300


def get_status_data(project):
    return project.tickets.values('status').annotate(
        count=Count('id')
    ).order_by('status')


def calculate_project_stats(project):
    # essential stats of the project
    cache_key = f'project_stats_{project.id}'
    cached_stats = cache.get(cache_key)

    if cached_stats is not None:
        return cached_stats
    today = timezone.now().date()
    week_from_now = today + timezone.timedelta(days=7)

    stats = {
        'total_tickets': project.tickets.count(),
        'active_tickets': project.tickets.filter(
            status__in=['open', 'in_progress']
        ).count(),
        'completed_tickets': project.tickets.filter(
            status__in=['resolved', 'closed']
        ).count(),
        'total_bugs': project.bugreports.count(),
        'pending_bugs': project.bugreports.filter(
            is_approved=False,
            status__in=['open', 'in_progress']
        ).count(),
        'due_soon':project.tickets.filter(
            status__in=['open', 'in_progress'],
            due_date__lte=week_from_now,
            due_date__gt=today,
        ).count()
    }

    cache.set(cache_key, stats, CACHE_TIMEOUT)
    return stats


def get_work_types_data(project):
    regular_tickets = project.tickets.filter(is_bug_ticket=False).count()
    bug_tickets = project.tickets.filter(is_bug_ticket=True).count()
    pending_bugs = project.bugreports.filter(is_approved=False).count()

    return {
        'regular_tickets': regular_tickets,
        'bug_tickets': bug_tickets,
        'pending_bugs': pending_bugs
    }


def get_team_workload_data(project):
    cache_key = f'team_workload_project_{project.id}'
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return cached_data

    team_data = []
    developers = project.members.filter(profile__role=UserRoleChoices.DEVELOPER)

    for member in developers:
        team_data.append({
            'Member': member.get_full_name(),
            'Active Tickets': project.tickets.filter(
                assigned_to=member,
                status__in=['open', 'in_progress']
            ).count(),
            'Total Assigned': project.tickets.filter(
                assigned_to=member
            ).count(),
            'Bug Tickets Assigned': project.tickets.filter(
                assigned_to=member,
                is_bug_ticket=True,
            ).count()
        })

    cache.set(cache_key, team_data, CACHE_TIMEOUT)
    return team_data
