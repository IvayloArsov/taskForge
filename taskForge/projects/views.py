from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

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
        if self.request.user.is_staff:
            return Project.objects.all()
        return Project.objects.filter(members=self.request.user)


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
        return (self.request.user.is_staff or
                self.request.user in project.members.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        show_type = self.request.GET.get('show', 'tickets')

        active_statuses = ['open', 'in_progress']
        completed_statuses = ['resolved', 'closed']

        # shows tickets that need to be approved/denied to staff/admin roles only
        if self.request.user.is_staff:
            context['pending_bugs'] = self.object.bugreports.filter(
                is_approved=False,
                status__in=active_statuses
            ).order_by('-created_at')


        # shows active & completed tickets
        if show_type == 'tickets':
            context['active_tickets'] = self.object.tickets.filter(
                status__in=active_statuses
            ).order_by('-created_at')

            context['completed_tickets'] = self.object.tickets.filter(
                status__in=completed_statuses
            ).order_by('-updated_at')

        # shows pending & ongoing bug reports
        if show_type == 'bugs':
            if self.request.user.is_staff:
                context['pending_bugs'] = self.object.bugreports.filter(
                    is_approved=False,
                    status__in=active_statuses
                ).order_by('-created_at')

            context['active_bugs'] = self.object.bugreports.filter(
                is_approved=True,
                status__in=active_statuses
            ).order_by('-created_at')

        context['show_type'] = show_type
        return context