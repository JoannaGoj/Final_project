from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now, timedelta

# Create your models here.


URGENT = (
    (1, 'max priority'),
    (2, 'urgent'),
    (3, 'not urgent'),

)


class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=250, blank=True)
    cancelled = models.BooleanField(default=False)
    updated_at = models.DateTimeField('%d.%m.%Y', null=True)
    start_time = models.DateTimeField("%d.%m.%Y,%H:%M", default=now)
    end_time = models.DateTimeField("%d.%m.%Y,%H:%M", default=now)
    tags = models.ManyToManyField('Tags')

    class Meta:
        abstract = True

    def is_approaching_or_past(self):
        is_past_or_approaching = ""
        comparing_start_date_to_today = (date.today() - self.start_time.date()).days
        if comparing_start_date_to_today < 0:
            is_past_or_approaching += 'Past'
            return is_past_or_approaching, comparing_start_date_to_today
        elif 0 <= comparing_start_date_to_today < 3:
            is_past_or_approaching += 'Soon approaching'
            lista = [is_past_or_approaching, comparing_start_date_to_today]
            return lista
        else:
            is_past_or_approaching += 'In future'
            return is_past_or_approaching, comparing_start_date_to_today

    def __str__(self):
        formatted_start_time = self.start_time.strftime("%H:%M")
        formatted_end_time = self.end_time.strftime("%H:%M")
        formatted_start_date = self.start_time.strftime('%d.%m.%Y')
        formatted_end_date = self.end_time.strftime('%d.%m.%Y')
        if formatted_end_date == formatted_start_date:
            return f"{formatted_start_date}  |  {formatted_start_time} - {formatted_end_time}"
        else:
            days_task_lasts = self.end_time - self.start_time
            formatted_days_task_lasts = days_task_lasts.days
            return f"{formatted_start_date} - {formatted_end_date} |  {formatted_start_time} - {formatted_end_time}(+{formatted_days_task_lasts})"


class Event(Schedule):

    def __str__(self):
        event_info_to_display = [self.name, self.description, self.date, self.start_time, self.end_time, self.tags]
        return event_info_to_display


class Task(Schedule):
    urgent = models.IntegerField(choices=URGENT, default=2)
    completed = models.BooleanField(default=False)


class Tags(models.Model):
    name = models.CharField(max_length=64)


class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    time = models.DateTimeField(default=now)
    created = models.DateTimeField(auto_now_add=True)
