from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from ..analytics.charts import (
    generate_priority_chart,
    generate_status_chart,
    generate_work_types_chart,
    generate_team_workload_chart,
)


class ProjectSummaryView(LoginRequiredMixin, DetailView):
    template_name = 'projects/project details/project-summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['view_type'] == 'summary':
            context.update({
                'priority_chart': generate_priority_chart(self.object),
                'status_chart': generate_status_chart(self.object),
                'work_types_chart': generate_work_types_chart(self.object),
                'team_workload_chart': generate_team_workload_chart(self.object)
            })
        return context
