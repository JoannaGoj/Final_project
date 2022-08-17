from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from django.urls import reverse_lazy


# Create your views here.


class Example(View):
    def get(self, request):
        return render(request, 'example_user_page.html')


class ShowUserPage(LoginRequiredMixin, View):
    def get(self, request):
        pass


class AddTaskView(CreateView):
    model = Task
    fields = ['name', 'description', 'user']
    template_name = 'form_template.html'
    success_url = reverse_lazy('example')


class ShowAllTasks(ListView):
    model = Task
    template_name = 'show_all_tasks.html'
    fields = '__all__'
