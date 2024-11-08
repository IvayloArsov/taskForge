from django.urls import path, include
from .views import CustomUserRegisterView, CustomUserLoginView, CustomLogoutView, ProfileDetailView
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', CustomUserRegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-details'),
]
