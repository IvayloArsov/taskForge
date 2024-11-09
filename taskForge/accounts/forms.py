from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from taskForge.accounts.models import Profile


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ' ',
            'id': 'floatingUsername'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': ' ',
            'id': 'floatingEmail'
        })
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ' ',
            'id': 'floatingFirstName'
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ' ',
            'id': 'floatingLastName'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ' ',
            'id': 'floatingPassword'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ' ',
            'id': 'floatingPasswordConfirm'
        })
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '',
        })
    )

    error_messages = {
        'invalid_login': 'Please enter a correct username and password. Note that both fields may be case-sensitive.',
        'inactive': 'This account is inactive.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = 'The username or password you entered is incorrect. Please try again.'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role']
        widgets = {
            'role': forms.Select(attrs={
                'class': 'form-control'
            })
        }