from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    description=forms.CharField(max_length=1000, widget=forms.Textarea(attrs={
            'rows': 10,
            'cols': 125,
            'style': 'resize:none;',
        }))

    class Meta:
        model = Task
        fields = ('title', 'category', 'description', 'current_status', 'publish_status')
        labels = {
            'title': 'Title',
            'category': 'Category',
            'description': 'Description',
            'current_status': 'Status',
            'publish_status': "Public status",
        }