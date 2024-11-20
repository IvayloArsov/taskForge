import asyncio

from asgiref.sync import sync_to_async
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

    async def get_context_data(self, **kwargs):
        context = await super().get_context_data(**kwargs)
        if context['view_type'] == 'summary':
            priority_chart = sync_to_async(generate_priority_chart)
            status_chart = sync_to_async(generate_status_chart)
            work_types_chart = sync_to_async(generate_work_types_chart)
            team_workload_chart = sync_to_async(generate_team_workload_chart)

            data = await asyncio.gather(
                priority_chart(self.object),
                status_chart(self.object),
                work_types_chart(self.object),
                team_workload_chart(self.object),
            )

            context.update({
                'priority_chart': data[0],
                'status_chart': data[1],
                'work_types_chart': data[2],
                'team_workload_chart': data[3],
            })

        return context
