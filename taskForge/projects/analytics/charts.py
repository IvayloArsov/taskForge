import pandas as pd
import plotly.express as px
from django.db.models import Count
from .utils import (
    get_status_data,
    get_work_types_data,
    get_team_workload_data
)


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
    df = pd.DataFrame({
        'Type': ['Regular Tickets', 'Bug Tickets', 'Pending Bug Reports'],
        'Count': [
            data['regular_tickets'],
            data['bug_tickets'],
            data['pending_bugs']
        ]
    })
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
    team_data = get_team_workload_data(project)
    df = pd.DataFrame(team_data)

    if not df.empty:
        fig = px.bar(
            df,
            x=['Active Tickets', 'Total Assigned', 'Pending Bugs'],
            y='Member',
            orientation='h',
            barmode='group'
        )

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            title_font_color='#94a3b8',
            legend_font_color='#94a3b8',
            template='plotly_dark',
            height=400,
            margin=dict(l=150),
            xaxis_title="Number of Items",
            yaxis_title=None
        )

        return fig.to_html()
    return ""
