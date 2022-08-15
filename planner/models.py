from datetime import date
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

URGENT = (
    (1, 'max priority'),
    (2, 'urgent'),
    (3, 'not urgent'),

)


class Timeblock(models.Model):
    start_time = models.DateTimeField('%H:%M')
    end_time = models.DateTimeField('%H:%M')

    # def how_much_time(self):
    #     timeblock = self.end_time - self.start_time
    #     return  # ???????


class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=250, blank=True)
    date = models.DateField(auto_now=True)
    cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    timeblock = models.ForeignKey(Timeblock, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Event(Schedule):

    def __str__(self):
        return self.name


class Task(Schedule):
    urgent = models.IntegerField(choices=URGENT)

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=64)
    task = models.ManyToManyField(Task)
    event = models.ManyToManyField(Event)


class Text(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Journal(Text):
    date = models.DateField(auto_now=True)

# class Routine(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=64)
#     description = models.TextField
#

# class Notes(Text):
#     pass
#
#
# class DailyPlanner(models.Model):
#     pass
