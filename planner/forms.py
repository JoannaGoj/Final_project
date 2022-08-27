from django.forms.widgets import TextInput, DateTimeInput, DateInput
from django import forms
from .models import Journal, Tags, Task, Event
from django.forms import ValidationError


class JournalInputEntryForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['date_of_entry','name', 'text']
        widgets = {'date_of_entry': DateTimeInput(attrs={'type': 'datetime-local'})}



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
        fields = ['name', 'description', 'tags', 'date', 'urgent']
        widgets = {'urgent': forms.RadioSelect,
                   'date': DateInput(attrs={
                       'placeholder': 'Select a date',
                       'type': 'date'}),
                   'tags': forms.CheckboxSelectMultiple()}


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'tags', 'start_time', 'end_time']
        widgets = {'start_time': DateTimeInput(attrs={'type': 'datetime-local'}),
                   'end_time': DateTimeInput(attrs={'type': 'datetime-local'}),
                    'tags': forms.CheckboxSelectMultiple()
        }

    def clean(self):
        data = super().clean()
        if data['end_time'] < data['start_time']:
            raise ValidationError('End time of event cannot be earlier than start time!')
        return data

