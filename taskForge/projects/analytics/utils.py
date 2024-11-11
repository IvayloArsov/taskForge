from django.db.models import Count

from taskForge.accounts.choices import UserRoleChoices


def get_status_data(project):
    return project.tickets.values('status').annotate(
        count=Count('id')
    ).order_by('status')


def calculate_project_stats(project):
    # will give us very useful information to implement 5th graph later
    return {
        'total_tickets': project.tickets.count(),
        'active_tickets': project.tickets.filter(status__in=['open', 'in_progress']).count(),
        'completed_tickets': project.tickets.filter(status__in=['resolved', 'closed']).count(),
        'total_bugs': project.bugreports.count(),
        'pending_bugs': project.bugreports.filter(is_approved=False).count(),
    }


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
            'Pending Bugs': project.bugreports.filter(
                created_by=member,
                is_approved=False
            ).count()
        })
    return team_data
