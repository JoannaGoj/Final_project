from datetime import date

from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task, Event, Journal
from django.urls import reverse_lazy
from itertools import chain
from .forms import JournalInputForm


# Create your views here.


class Example(View):
    def get(self, request):
        tasks = Task.objects.all()
        return render(request, 'example_user_page.html', {'tasks': tasks})



class AddTaskView(CreateView):
    model = Task
    fields = ['name', 'description', 'user']
    template_name = 'form_template.html'
    success_url = reverse_lazy('example')


class AddEventView(CreateView):
    model = Event
    fields = ['name', 'description', 'user']
    template_name = 'form_template.html'
    success_url = reverse_lazy('example')

class AddJournalEntryView(CreateView):
    model = Journal
    fields = ['name', 'text', 'user']
    template_name = 'form_template.html'
    success_url = reverse_lazy('example')

class ShowAllTasks(ListView):
    model = Task
    template_name = 'show_all_tasks.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update({'model': 'tasks'})
        return data


class ShowAllEvents(ListView):
    model = Event
    template_name = 'show_all_events.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update({'model': 'events'})
        return data


# need to prevent page refresh after posting journal notes
class UserDailyPlanner(View):
    def get(self, request):
        today = date.today()
        tasks = Task.objects.filter(start_time=today) #user_Id dodać
        events = Event.objects.filter(start_time=today)
        journal = Journal.objects.filter(date_of_entry=today)
        all_items_on_the_page = list(chain(tasks, events, journal))
        journal_form = JournalInputForm
        return render(request, 'user_page.html', {'items': all_items_on_the_page, 'journal_form': journal_form})
