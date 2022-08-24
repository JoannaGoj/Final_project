from datetime import date
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task, Event, Journal, Tags
from django.urls import reverse_lazy, reverse
from itertools import chain
from .forms import JournalInputForm, TagsForm, EventForm


# Create your views here.


class Example(View):
    def get(self, request):
        tasks = Task.objects.all()
        return render(request, 'example_user_page.html', {'tasks': tasks})


class AddTaskView(CreateView):
    pass


class ManageEventsView(View):
    def get(self, request):
        form = EventForm
        return render(request, 'manage_events.html', {'form': form})

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
        return render(request, reverse('show_all_events'))



class AddJournalEntryView(CreateView):
    model = Journal
    fields = ['name', 'text', 'user']
    template_name = 'form_template.html'
    success_url = reverse_lazy('example')


class ManageTags(View):
    def get(self, request):
        tags = Tags.objects.all().order_by()
        form = TagsForm
        events = Event.objects.all()
        return render(request, 'manage_tags.html', {'tags': tags, 'form': form, 'events':events})

    def post(self, request):
        form = TagsForm(request.POST)
        tags = Tags.objects.all().order_by()
        if form.is_valid():
            form.save()
        return render(request, 'manage_tags.html', {'tags': tags, 'form': form})


class UpdateTag(UpdateView):
    model = Tags
    form_class = TagsForm
    template_name = 'manage_tags.html'
    success_url = reverse_lazy("manage_tags")

    def get_context_data(self, **kwargs):
        all_tags = Tags.objects.all()
        data = super().get_context_data(**kwargs)
        data.update({'tags': all_tags})
        return data

# czemu pierwszy przycisk delete zjezdza na doł? Trzeba to poprawic
class DeleteTagView(View):
    def get(self, request, pk):
        form = TagsForm
        all_tags = Tags.objects.all()
        return render(request, 'manage_tags.html', {'tags': all_tags, 'message': "delete", 'tag_pk': pk, 'form': form})

    def post(self, request, pk):
        tag_to_delete = Tags.objects.get(id=pk)
        tag_to_delete.delete()
        return redirect(reverse('manage_tags'))


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
    template_name = 'manage_events.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update({'model': 'events'})
        return data


# need to prevent page refresh after posting journal notes
class UserDailyPlanner(View):
    def get(self, request):
        today = date.today()
        # user_Id dodać
        events = Event.objects.filter(start_time=today)
        journal = Journal.objects.filter(date_of_entry=today)
        all_items_on_the_page = list(chain(events, journal)) # dodac taski
        journal_form = JournalInputForm
        return render(request, 'user_page.html', {'items': all_items_on_the_page, 'journal_form': journal_form})
