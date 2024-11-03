from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import CustomUserRegisterView, CustomUserLoginView, CustomLogoutView

urlpatterns = [
    path('register/', CustomUserRegisterView.as_view(), name='register'),
    path('login/', CustomUserLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout')
]
