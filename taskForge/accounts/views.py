from audioop import reverse

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from taskForge.accounts.forms import CustomUserCreationForm, UserLoginForm, ProfileForm
from taskForge.accounts.models import Profile


class CustomUserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('index')


class CustomUserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('index')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/profile-details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object.user
        context['assigned_tickets'] = user.assigned_tickets.all()
        context['created_tickets'] = user.created_tickets.all()
        context['projects'] = user.projects.all()
        return context

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('pk')
        return Profile.objects.get(user_id=user_id)
