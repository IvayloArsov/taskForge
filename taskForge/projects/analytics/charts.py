import pandas as pd
import plotly.express as px
from django.db.models import Count
from .utils import (
    get_status_data,
    get_work_types_data,
    get_team_workload_data
)
from ...accounts.choices import UserRoleChoices


def generate_priority_chart(project):
    tickets = project.tickets.all()
    priority_data = tickets.values('priority').annotate(
        count=Count('id')
    ).order_by('priority')
    df = pd.DataFrame(priority_data)

    if not df.empty:
        fig = px.pie(
            df,
            values='count',
            names='priority',
            category_orders={"priority": ["low", "medium", "high", "urgent"]},
            color='priority',
            color_discrete_map={
                "low": "#22c55e",
                "medium": "#fbbf24",
                "high": "#ef4444",
                "urgent": "#dc2626"
            },
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            title_font_color='#94a3b8',
            legend_font_color='#94a3b8',
            template='plotly_dark',
        )
        return fig.to_html()

    return ''


def generate_status_chart(project):
    status_data = get_status_data(project)
    df = pd.DataFrame(status_data)

    if not df.empty:
        fig = px.bar(
            df,
            x='status',
            y='count',
            color='status',
            color_discrete_map={
                'open': '#3b82f6',
                'in_progress': '#8b5cf6',
                'resolved': '#10b981',
                'closed': '#6b7280',
            }
        )

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            title_font_color='#94a3b8',
            legend_font_color='#94a3b8',
            template='plotly_dark',
            xaxis_title="Status",
            yaxis_title="Number of Tickets"
        )

        return fig.to_html()
    return ""


def generate_work_types_chart(project):
    data = get_work_types_data(project)

    if sum(data.values()) == 0:
        return ''

    df = pd.DataFrame({
        'Type': ['Regular Tickets', 'Bug Tickets', 'Pending Bug Reports'],
        'Count': [
            data['regular_tickets'],
            data['bug_tickets'],
            data['pending_bugs']
        ]
    })
    if not df.empty:
        fig = px.bar(
            df,
            x='Type',
            y='Count',
            color='Type',
            color_discrete_map={
                'Regular Tickets': '#3b82f6',
                'Bug Tickets': '#ef4444',
                'Pending Bug Reports': '#f59e0b'
            }
        )

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            title_font_color='#94a3b8',
            legend_font_color='#94a3b8',
            template='plotly_dark',
            showlegend=False
        )

    return fig.to_html()


def generate_team_workload_chart(project):
    team_data = []
    developers = project.members.filter(profile__role=UserRoleChoices.DEVELOPER)
    unassigned_count = project.tickets.filter(assigned_to=None).count()

    total_tickets = project.tickets.count()
    unassigned_percentage = (unassigned_count/total_tickets*100) if total_tickets > 0 else 0

    team_data.append({
        'Member':'Unassigned',
        'Work': unassigned_percentage
    })

    for member in developers:
        assigned_count = project.tickets.filter(assigned_to=member).count()
        percentage = (assigned_count/total_tickets*100) if total_tickets > 0 else 0
        team_data.append({
            'Member': member.get_full_name(),
            'Work': percentage
        })

    if team_data:
        df = pd.DataFrame(team_data)
        fig = px.bar(
            df,
            x='Work',
            y='Member',
            text='Work',
            orientation='h'
        )

        fig.update_traces(
            texttemplate='%{text:.0f}%',
            textposition='auto',
        )

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            title_font_color='#94a3b8',
            legend_font_color='#94a3b8',
            template='plotly_dark',
            xaxis_title="Workload (%)",
            yaxis_title=None,
            showlegend=False
        )

        return fig.to_html()
    return ""