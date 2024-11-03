from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from taskForge.accounts.forms import CustomUserCreationForm, UserLoginForm


# Create your views here.
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