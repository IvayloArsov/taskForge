import plotly.graph_objects as go
import plotly.express as px
from .utils import (
    get_status_data,
    get_work_types_data,
    get_team_workload_data
)


def generate_priority_chart(project):
    priorities = {"low": 0, "medium": 0, "high": 0, "urgent": 0}
    for ticket in project.tickets.all():
        priorities[ticket.priority] += 1

    if not any(priorities.values()):
        return ''

    fig = px.pie(
        names=list(priorities.keys()),
        values=list(priorities.values()),
        color=list(priorities.keys()),
        color_discrete_map={
            "low": "#22c55e",
            "medium": "#fbbf24",
            "high": "#ef4444",
            "urgent": "#dc2626"
        }
    )
    fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)')
    return fig.to_html()


def generate_status_chart(project):
    status_data = get_status_data(project)
    if not status_data:
        return ""

    status_labels = {
        'open': 'Open',
        'in_progress': 'In Progress',
        'resolved': 'Resolved',
        'closed': 'Closed'
    }

    fig = px.bar(
        x=[status_labels[s['status']] for s in status_data],
        y=[s['count'] for s in status_data],
        color=[status_labels[s['status']] for s in status_data],
        color_discrete_map={
            'Open': '#3b82f6',
            'In Progress': '#8b5cf6',
            'Resolved': '#10b981',
            'Closed': '#6b7280',
        }
    )

    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Status",
        yaxis_title="Number of Tickets",
        showlegend=False
    )
    return fig.to_html()


def generate_work_types_chart(project):
    data = get_work_types_data(project)

    if not any(data.values()):
        return ''

    fig = go.Figure(data=[go.Pie(
        labels=['Regular Tickets', 'Bug Tickets'],
        values=[data['regular_tickets'], data['bug_tickets']],
        hole=.4,
    )])

    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=True
    )
    return fig.to_html()


def generate_team_workload_chart(project):
    team_data = get_team_workload_data(project)
    if not team_data:
        return ""

    colors = ['#ef4444' if d['Member'] == 'Unassigned' else '#3b82f6' for d in team_data]

    fig = go.Figure(go.Bar(
        x=[d['Work Count'] for d in team_data],
        y=[d['Member'] for d in team_data],
        text=[d['Label'] for d in team_data],
        orientation='h',
        textposition='auto',
        marker_color = colors,
    ))

    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Workload",
        yaxis_title=None,
        showlegend=False,
    )
    return fig.to_html()
