from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from .forms import TicketForm, BugReportForm
from .models import Ticket, BugReport
from taskForge.projects.models import Project
from ..comments.forms import CommentForm


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/ticket-list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(project__members=self.request.user)


class TicketDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Ticket
    template_name = 'tickets/ticket details/ticket-details.html'
    context_object_name = 'ticket'

    def test_func(self):
        ticket = self.get_object()
        return (self.request.user.is_staff or
                self.request.user in ticket.project.members.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/ticket-create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        project_id = self.request.GET.get('project')
        if project_id:
            kwargs['initial_project_id'] = project_id
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tickets:details', kwargs={'pk': self.object.pk})


class TicketUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/ticket-edit.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        ticket = self.get_object()
        return (self.request.user.is_staff or
                self.request.user == ticket.created_by or
                self.request.user == ticket.assigned_to)

    def get_success_url(self):
        return reverse_lazy('tickets:details', kwargs={'pk': self.object.pk})


class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    template_name = 'tickets/ticket-delete.html'
    success_url = reverse_lazy('tickets:list')

    def test_func(self):
        """
        Only Ticket creator or Admin/Manager can delete
        """
        ticket = self.get_object()
        return (
                self.request.user.is_staff or
                self.request.user == ticket.created_by
        )


class BugReportCreateView(LoginRequiredMixin, CreateView):
    model = BugReport
    form_class = BugReportForm
    template_name = 'tickets/bug-report-creation.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('projects:details', kwargs={'pk': self.object.project.pk})


class BugReportApproveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.is_staff:
            raise PermissionDenied

        bug = get_object_or_404(BugReport, pk=pk)
        bug.is_approved = True
        bug.save()

        return redirect('projects:details', pk=bug.project.pk)


class BugReportDenyView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.is_staff:
            raise PermissionDenied

        bug = get_object_or_404(BugReport, pk=pk)
        bug.is_approved = False
        bug.status = 'closed'
        bug.save()

        return redirect('projects:details', pk=bug.project.pk)


class BugReportDetailView(LoginRequiredMixin, DetailView):
    model = BugReport
    template_name = 'tickets/bug-report-details.html'
    context_object_name = 'bug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
