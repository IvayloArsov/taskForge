from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone

from taskForge.accounts.choices import UserRoleChoices
from taskForge.projects.analytics.charts import (
    generate_priority_chart,
    generate_status_chart,
    generate_work_types_chart,
    generate_team_workload_chart
)
from taskForge.projects.forms import ProjectForm
from taskForge.projects.models import Project


class ProjectListView(LoginRequiredMixin, ListView):
    """
    Visible to all authenticated users that belong to the project
    Staff and Admin can see full list of the Projects, and can do full crud
    """
    model = Project
    template_name = 'projects/project-list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Project.objects.all()
        elif user.profile.role == UserRoleChoices.END_USER:
            return Project.objects.filter(members=user)
        else:
            return Project.objects.filter(members=user)


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class ProjectCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    """
    Staff and Admin can do full crud
    This is invisible to lower users
    """
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project-creation.html'
    success_url = reverse_lazy('projects:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    """
    Only staff and admin can do full crud
    """
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project-edit.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('projects:details', kwargs={'pk': self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('projects:list')

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        return result


class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Project
    template_name = 'projects/project details/project-details.html'
    context_object_name = 'project'

    def test_func(self):
        project = self.get_object()
        user = self.request.user
        return user.is_staff or user in project.members.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_type = self.request.GET.get('view', 'summary')
        context['view_type'] = view_type
        context['now'] = timezone.now().date()

        sort_by = self.request.GET.get('sort', '-created_at')
        sort_direction = self.request.GET.get('direction', 'asc')

        context['current_sort'] = sort_by
        context['current_direction'] = sort_direction

        sort_field = f'-{sort_by}' if sort_direction == 'desc' else sort_by

        if view_type == 'board':
            context['tickets'] = self.object.tickets.exclude(
                status__in=['closed', 'resolved']
            ).order_by(sort_field)

            if self.request.user.is_staff:
                context['pending_bugs'] = self.object.bugreports.filter(
                    is_approved=False
                ).order_by(sort_field)

        elif view_type == 'archived':
            context['archived_tickets'] = self.object.tickets.filter(
                status__in=['closed', 'resolved']
            ).order_by(sort_field)

        elif view_type == 'summary':
            try:
                from ..analytics.utils import calculate_project_stats
                context['project_stats'] = calculate_project_stats(self.object)

                context.update({
                    'priority_chart': generate_priority_chart(self.object),
                    'status_chart': generate_status_chart(self.object),
                    'work_types_chart': generate_work_types_chart(self.object),
                    'team_workload_chart': generate_team_workload_chart(self.object)
                })
            except Exception as e:
                print(f"Error generating analytics: {e}")
                context['analytics_error'] = "Unable to load analytics data"

        context['is_end_user'] = self.request.user.profile.role == UserRoleChoices.END_USER
        return context
