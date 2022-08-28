from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task, Event, Journal, Tags
from django.urls import reverse_lazy, reverse
from itertools import chain
from .forms import JournalInputEntryForm, TagsForm, EventForm, TaskForm
from datetime import datetime


# Create your views here.

class RedirectToDailyPlanner(View):
    def get(self, request):
        today = datetime.now()
        return redirect(reverse('daily_planner', kwargs={'year': today.year, 'month': today.month, 'day': today.day}))


class ManageTasksView(LoginRequiredMixin, View):
    def get(self, request):
        form = TaskForm
        user = request.user
        tasks = Task.objects.filter(user_id=user.id).order_by('-date')
        return render(request, 'manage_tasks.html', {'form': form, 'tasks': tasks})

    def post(self, request):
        form = TaskForm(request.POST)
        user = request.user
        tasks = Task.objects.filter(user_id=user.id).order_by('-date')
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('manage_tasks')
        return render(request, 'manage_tasks.html', {'form': form, 'tasks': tasks})


class UpdateTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'manage_tasks.html'
    success_url = reverse_lazy("manage_tasks")

    def get_context_data(self, **kwargs):
        user = self.request.user
        tasks = Task.objects.filter(user_id=user.id).order_by('-date')
        data = super().get_context_data(**kwargs)
        data.update({'tasks': tasks})
        return data


class DeleteTaskView(LoginRequiredMixin, View):
    def get(self, request, pk):
        form = TaskForm
        user = self.request.user
        tasks = Task.objects.filter(user_id=user.id).order_by('-date')
        return render(request, 'manage_tasks.html',
                      {'tasks': tasks, 'confirm_delete': "delete", 'task_pk': pk, 'form': form})

    def post(self, request, pk):
        task_to_delete = Task.objects.get(id=pk)
        task_to_delete.delete()
        return redirect('manage_tasks')



class ManageEventsView(LoginRequiredMixin, View):
    def get(self, request):
        form = EventForm
        user = request.user
        events = Event.objects.filter(user_id=user.id).order_by('-start_time')
        return render(request, 'manage_events.html', {'form': form, 'events': events})

    def post(self, request):
        form = EventForm(request.POST)
        user = request.user
        events = Event.objects.filter(user_id=user.id).order_by('-start_time')
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('manageevents')
        return render(request, 'manage_events.html', {'form': form, 'events': events})


class UpdateEventView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'manage_events.html'
    success_url = reverse_lazy("manageevents")

    def get_context_data(self, **kwargs):
        user = self.request.user
        events = Event.objects.filter(user_id=user.id).order_by('-start_time')
        data = super().get_context_data(**kwargs)
        data.update({'events': events})
        return data


class DeleteEventView(LoginRequiredMixin, View):
    def get(self, request, pk):
        form = EventForm
        user = self.request.user
        events = Event.objects.filter(user_id=user.id).order_by('-start_time')
        return render(request, 'manage_events.html',
                      {'events': events, 'confirm_delete': "delete", 'event_pk': pk, 'form': form})

    def post(self, request, pk):
        event_to_delete = Event.objects.get(id=pk)
        event_to_delete.delete()
        return redirect('manageevents')


class ShowAllJournalView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        form = JournalInputEntryForm
        user_journal_entries = Journal.objects.filter(user_id=user.id)
        return render(request, 'show_all_journal_entries.html',
                      {'user_journal_entries': user_journal_entries, 'form': form})

    def post(self, request):
        form = JournalInputEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('show_all_journal_entries')
        return render(request, 'show_all_journal_entries.html', {'form': form})


class UpdateJournalEntryView(LoginRequiredMixin, UpdateView):
    model = Journal
    form_class = JournalInputEntryForm
    template_name = 'show_all_journal_entries.html'
    success_url = reverse_lazy("show_all_journal_entries")

    def get_context_data(self, **kwargs):
        user_journal_entries = Journal.objects.filter(user=self.request.user)
        data = super().get_context_data(**kwargs)
        data.update({'user_journal_entries': user_journal_entries})
        return data


class DeleteJournalEntryView(LoginRequiredMixin, View):
    def get(self, request, pk):
        form = JournalInputEntryForm
        user = request.user
        user_journal_entries = Journal.objects.filter(user_id=user.id)
        return render(request, 'show_all_journal_entries.html',
                      {'user_journal_entries': user_journal_entries, 'form': form, 'entry_pk': pk, 'message': "delete"})

    def post(self, request, pk):
        entry_to_delete = Journal.objects.get(id=pk)
        entry_to_delete.delete()
        return redirect('show_all_journal_entries')


class ManageTags(LoginRequiredMixin, View):
    def get(self, request):
        tags = Tags.objects.all()
        form = TagsForm
        return render(request, 'manage_tags.html', {'tags': tags, 'form': form})

    def post(self, request):
        form = TagsForm(request.POST)
        tags = Tags.objects.all()
        if form.is_valid():
            form.save()
            return redirect('manage_tags')
        return render(request, 'manage_tags.html', {'tags': tags, 'form': form})


class UpdateTag(LoginRequiredMixin, UpdateView):
    model = Tags
    form_class = TagsForm
    template_name = 'manage_tags.html'
    success_url = reverse_lazy("manage_tags")

    def get_context_data(self, **kwargs):
        all_tags = Tags.objects.all()
        data = super().get_context_data(**kwargs)
        data.update({'tags': all_tags})
        return data


class DeleteTagView(LoginRequiredMixin, View):
    def get(self, request, pk):
        form = TagsForm
        all_tags = Tags.objects.all()
        return render(request, 'manage_tags.html', {'tags': all_tags, 'message': "delete", 'tag_pk': pk, 'form': form})

    def post(self, request, pk):
        tag_to_delete = Tags.objects.get(id=pk)
        tag_to_delete.delete()
        return redirect('manage_tags')


class ShowAllTasks(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'show_all_tasks.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update({'model': 'tasks'})
        return data



class UserDailyPlanner(LoginRequiredMixin, View):
    def get(self, request, year, month, day):
        user = request.user
        events = Event.objects.filter(start_time__day__lte=day, start_time__month__lte=month,
                                      start_time__year__lte=year, end_time__day__gte=day,
                                      end_time__month__gte=month, end_time__year__gte=year, user_id=user.id)
        journal = Journal.objects.filter(date_of_entry__day=day, date_of_entry__month=month,
                                         date_of_entry__year=year, user_id=user.id)
        tasks = Task.objects.filter(date__year=year, date__month=month, date__day=day, user_id=user.id)
        all_items_on_the_page = list(chain(events, journal, tasks))
        journal_form = JournalInputEntryForm
        today = datetime.now()
        context = {"items": all_items_on_the_page,
                   "journal_form": journal_form,
                   "todays_date": today
                   }
        return render(request, 'user_page.html', context)

    def post(self, request, day, month, year):
        form = JournalInputEntryForm(request.POST)
        user = request.user
        events = Event.objects.filter(start_time__day__lte=day, start_time__month__lte=month,
                                      start_time__year__lte=year, end_time__day__gte=day,
                                      end_time__month__gte=month, end_time__year__gte=year, user_id=user.id)
        journal = Journal.objects.filter(date_of_entry__day=day, date_of_entry__month=month,
                                         date_of_entry__year=year, user_id=user.id)
        tasks = Task.objects.filter(date__year=year, date__month=month, date__day=day, user_id=user.id)
        all_items_on_the_page = list(chain(events, journal, tasks))
        journal_form = JournalInputEntryForm
        today = datetime.now()
        context = {"items": all_items_on_the_page,
                   "journal_form": journal_form,
                   "todays_date": today
                   }
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect(reverse('daily_planner', kwargs={'year':year, 'month':month, 'day':day}))
        return render(request, 'user_page.html', context)
