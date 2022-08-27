"""Projekt_koncowy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView
from planner import views

year = 5
urlpatterns = [
    path('', views.RedirectToDailyPlanner.as_view(), name='redirect_to_daily_planner'),
    path('all_tasks/', views.ShowAllTasks.as_view(), name='show_all_tasks'),
    path('manage_events/', views.ManageEventsView.as_view(), name='manageevents'),
    path('update_event/<int:pk>/', views.UpdateEventView.as_view(), name="update_event"),
    path('delete_event/<int:pk>/', views.DeleteEventView.as_view(), name="delete_event"),
    path('daily_planner/<int:year>/<int:month>/<int:day>/', views.UserDailyPlanner.as_view(), name='daily_planner'),
    path('manage_tags/', views.ManageTags.as_view(), name='manage_tags'),
    path('update_tag/<int:pk>/', views.UpdateTag.as_view(), name='update_tag'),
    path('delete_tag/<int:pk>/', views.DeleteTagView.as_view(), name='delete_tag'),
    path('show_all_journal_entries/', views.ShowAllJournalView.as_view(), name='show_all_journal_entries'),
    path('update_journal_entry/<int:pk>/', views.UpdateJournalEntryView.as_view(), name='update_journal_entry'),
    path('delete_journal_entry/<int:pk>/', views.DeleteJournalEntryView.as_view(), name='delete_journal_entry'),
    path('manage_tasks/', views.ManageTasksView.as_view(), name='manage_tasks'),
    path('update_task/<int:pk>/', views.UpdateTaskView.as_view(), name="update_task"),
    path('delete_task/<int:pk>/', views.DeleteTaskView.as_view(), name="delete_task")
]
