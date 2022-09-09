# Create your views here.
from datetime import datetime

from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse, reverse_lazy
from accounts.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout


class Login(View):
    def get(self, request):
        form = LoginForm
        return render(request, 'form_template.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                today = datetime.now()
                year = today.year
                month = today.month
                day = today.day
                url = request.GET.get('next',
                                      reverse('daily_planner', kwargs={'year': year, 'month': month, 'day': day}))
                return redirect(url)
        else:
            form = LoginForm
        return render(request, 'form_template.html', {'form': form, 'message': 'Invalid login or password'})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm
        return render(request, 'form_template.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            register = form.save(commit=False)
            register.set_password(form.cleaned_data['password'])
            register.save()
            return redirect('login')
        return render(request, 'form_template.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
