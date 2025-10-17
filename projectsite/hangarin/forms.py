from django.forms import ModelForm
from django import forms
from .models import Task, SubTask, Category, Priority, Note


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'priority', 'status', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'deadline': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M:%S',
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                    'step': '1'  # allow seconds precision; prevents browser from rejecting nearby values
                }
            ),
        }

    # Accept datetime-local values including seconds
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M:%S', attrs={'type': 'datetime-local', 'class': 'form-control', 'step': '1'}),
        input_formats=['%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M']
    )


class SubTaskForm(ModelForm):
    class Meta:
        model = SubTask
        fields = ['title', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class SubTaskWithParentForm(ModelForm):
    class Meta:
        model = SubTask
        fields = ['title', 'status', 'parent_task']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'parent_task': forms.Select(attrs={'class': 'form-control'}),
        }


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PriorityForm(ModelForm):
    class Meta:
        model = Priority
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class NoteWithTaskForm(ModelForm):
    class Meta:
        model = Note
        fields = ['task', 'content']
        widgets = {
            'task': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
