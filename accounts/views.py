# Create your views here.
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse, reverse_lazy
from accounts.forms import LoginForm, CreateUserForm
from django.contrib.auth import authenticate, login


# można

class Login(View):
    def get(self, request):
        form = LoginForm
        print('0')
        return render(request, 'form_template.html', {'form':form})

    def post(self, request):
        form = LoginForm(request.POST)
        print('1')
        if form.is_valid():
            print('2')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username, password=password)
            print('3')
            if user is not None:
                print('4')
                login(request, user)
                url = request.GET.get('next', reverse('manage_tags'))
                print('5')
                return redirect(url)
        else:
            print('6')
            form = LoginForm
        return render(request, 'form_template.html', {'form': form, 'message':'nope'})



