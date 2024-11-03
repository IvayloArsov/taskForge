from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy

from taskForge.projects.models import Project


class ProjectListView(LoginRequiredMixin, ListView):
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
    model = Project
    template_name = 'projects/project-creation.html'
    fields = [
        'name',
        'description',
        'lead_by',
        'members'
    ]
    success_url = reverse_lazy('projects:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ProjectDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    context_object_name = 'project'