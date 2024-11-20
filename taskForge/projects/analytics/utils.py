from django.utils import timezone

from django.db.models import Count

from taskForge.accounts.choices import UserRoleChoices


def get_status_data(project):
    return project.tickets.values('status').annotate(
        count=Count('id')
    ).order_by('status')


def calculate_project_stats(project):
    # essential stats of the project

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
        'due_soon': project.tickets.filter(
            status__in=['open', 'in_progress'],
            due_date__lte=week_from_now,
            due_date__gt=today,
        ).count()
    }

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
    team_data = []
    developers = project.members.filter(profile__role=UserRoleChoices.DEVELOPER)
    unassigned_count = project.tickets.filter(assigned_to=None).count()

    total_tickets = project.tickets.filter(
        status__in=['open', 'in_progress']
    ).count()
    unassigned_percentage = (unassigned_count / total_tickets * 100) if total_tickets > 0 else 0

    team_data.append({
        'Member': 'Unassigned',
        'Work Count': unassigned_count,
        'Work Percentage': unassigned_percentage,
        'Label': f"{unassigned_count} ({unassigned_percentage:.1f})"
    })

    for member in developers:
        assigned_count = project.tickets.filter(
            assigned_to=member,
            status__in=['open', 'in_progress']

        ).count()
        percentage = (assigned_count / total_tickets * 100) if total_tickets > 0 else 0
        team_data.append({
            'Member': member.get_full_name(),
            'Work Count': assigned_count,
            'Work Percentage': percentage,
            'Label': f"{assigned_count} ({percentage:.1f}%)"

        })

    return team_data
