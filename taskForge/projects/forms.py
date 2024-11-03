from django import forms
from .models import Project


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
        self.fields['lead_by'].widget.attrs.update({
            'class':'form-control'
        })
        self.fields['members'].widget.attrs.update({
            'class':'form-control',
            'size': '5'
        })

