from django import forms
from django.contrib.auth import get_user_model
from setuptools.command.develop import develop

from .models import Project
from ..accounts.choices import UserRoleChoices
from ..accounts.models import Profile

User = get_user_model()


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name',
            'description',
            'lead_by',
            'members'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        manager_profiles = Profile.objects.filter(role=UserRoleChoices.MANAGER)
        manager_users = [profile.user for profile in manager_profiles]

        developer_profiles = Profile.objects.filter(role=UserRoleChoices.DEVELOPER)
        developer_users = [profile.user for profile in developer_profiles]

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter project name'
        })
        self.fields['description'].widget = forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the project...'
            }
        )
        # filter out only managers to be selectable for project's lead
        self.fields['lead_by'].queryset = User.objects.filter(id__in=[user.id for user in manager_users])
        self.fields['lead_by'].widget.attrs.update({
            'class': 'form-control'
        })

        # filter out only developers to be selectable for this field
        self.fields['members'].queryset=User.objects.filter(id__in=[user.id for user in developer_users])
        self.fields['members'].widget.attrs.update({
            'class': 'form-control',
            'size': '5'
        })
