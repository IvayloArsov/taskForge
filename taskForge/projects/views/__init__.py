from .project_views import (
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView
)

from .analytics_views import (
    ProjectSummaryView,
)

__all__ = [
    'ProjectListView',
    'ProjectDetailView',
    'ProjectCreateView',
    'ProjectUpdateView',
    'ProjectDeleteView',
    'ProjectSummaryView',
]
