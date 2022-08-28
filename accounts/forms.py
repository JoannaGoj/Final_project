from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128,
                               widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username']

    def clean(self):
        data = super().clean()
        if data['password'] != data['password2']:
            raise ValidationError('Passwords do not match!')
        return data