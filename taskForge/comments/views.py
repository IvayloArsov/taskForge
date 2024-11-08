from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.template.defaulttags import comment
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView

from taskForge.comments.forms import CommentForm
from taskForge.comments.models import Comment
from taskForge.tickets.models import Ticket


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    http_method_names = 'post'
    template_name = 'comments/comments.html'

    def form_valid(self, form):
        ticket = get_object_or_404(Ticket, pk=self.kwargs['ticket_id'])
        form.instance.ticket = ticket
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tickets:details', kwargs={'pk':self.kwargs['ticket_id']})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('tickets:details', kwargs={'pk':self.object.ticket.pk})
