# Create your views here.
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse, reverse_lazy
from accounts.forms import LoginForm
from django.contrib.auth import authenticate, login


# można

class Login(View):
    def get(self, request):
        form = LoginForm
        return render(request, 'form_template.html', {'form':form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,
                                username=username,
                                password=password)
            if user is not None:
                login(request, user)
                url = request.GET.get('next', reverse('login'))
                return redirect(url)
        return render(request, 'form_template.html', {'form': LoginForm(), 'message': 'invalid login details'})


