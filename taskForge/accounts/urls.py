from django.urls import path
from django.contrib.auth import views
from .views import CustomUserRegisterView, ProfileDetailView

app_name = 'accounts'

urlpatterns = [
    path('register/', CustomUserRegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-details'),
    path('password-reset/', 
         views.PasswordResetView.as_view(
             template_name='password_reset/password-reset-form.html',

             email_template_name='emails/password-reset.txt',
             html_email_template_name='emails/password-reset.html',

             subject_template_name='emails/password_reset_subject.txt',
             success_url='/accounts/password-reset/done/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         views.PasswordResetDoneView.as_view(
             template_name='password_reset/password-reset-done.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         views.PasswordResetConfirmView.as_view(
             template_name='password_reset/password-reset-confirm.html',
             success_url='/accounts/reset/done/'
         ),
         name='password_reset_confirm'),
    path('reset/done/',
         views.PasswordResetCompleteView.as_view(
             template_name='password_reset/password-reset-complete.html'
         ),
         name='password_reset_complete'),
]