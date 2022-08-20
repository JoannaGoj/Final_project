from django.forms.widgets import TextInput
from django import forms
from .models import Journal, Tags


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
