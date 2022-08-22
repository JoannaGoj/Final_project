from django.forms.widgets import TextInput, DateTimeInput
from django import forms
from .models import Journal, Tags, Task, Event


class JournalInputForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['name', 'text']


class TagsForm(forms.ModelForm):
    class Meta:
        model = Tags
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'tags', 'urgent']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'tags', 'start_time', 'end_time']
        widgets = {'start_time': DateTimeInput(attrs={'type': 'datetime-local'}),
                   'end_time': DateTimeInput(attrs={'type': 'datetime-local'}),
                    'tags': forms.CheckboxSelectMultiple()
        }
