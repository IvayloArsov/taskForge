from .models import Ticket, BugReport
from django import forms
from taskForge.projects.models import Project
from ..accounts.choices import UserRoleChoices
from ..accounts.models import Profile


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'title',
            'description',
            'priority',
            'status',
            'project',
            'assigned_to',
            'due_date'
        ]
        widgets = {
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Describe the issue...'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        initial_project_id = kwargs.pop('initial_project_id', None)
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter ticket title'
        })
        self.fields['priority'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['status'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['project'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['assigned_to'].widget.attrs.update({
            'class': 'form-control'
        })

        if user and not user.is_staff:
            self.fields['project'].queryset = Project.objects.filter(members=user)
            # only shows project members in the assigned_to field
            project = self.instance.project if self.instance.pk else None
            if project:
                self.fields['assigned_to'].queryset = project.members.all()

        if initial_project_id:
            # selects the same project when a ticket is being created from the project/id/details view
            try:
                project = Project.objects.get(pk=initial_project_id)
                self.fields['project'].initial = project
                self.fields['assigned_to'].queryset = project.members.all()
            except Project.DoesNotExist:
                pass

        self.fields['due_date'].help_text = "When should this ticket be completed?"
        self.fields['assigned_to'].help_text = "Who should work on this ticket?"
        self.fields['priority'].help_text = "How urgent is this ticket?"

    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get('project')
        assigned_to = cleaned_data.get('assigned_to')

        if project and assigned_to and assigned_to not in project.members.all():
            self.add_error('assigned_to',
                           'The assigned user must be a member of the project.')
        return cleaned_data


class BugReportForm(forms.ModelForm):
    class Meta:
        model = BugReport
        fields = ['title', 'description', 'project', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description of the bug'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Please include:\n- Steps to reproduce\n- Expected behavior\n- Actual behavior'
            }),
            'project': forms.Select(attrs={
                'class': 'form-control'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['project'].queryset = Project.objects.filter(members=user)
