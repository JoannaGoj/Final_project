from django import forms
from .models import Journal


class JournalInputForm(forms.ModelForm):

    class Meta:
        model = Journal
        fields = ['name', 'text']