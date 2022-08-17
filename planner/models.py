from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


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
    date = models.DateField(auto_now=True)
    cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField('%H:%M')
    end_time = models.DateTimeField('%H:%M')
    tags = models.ManyToManyField('Tags')

    class Meta:
        abstract = True


class Event(Schedule):

    def __str__(self):
        return self.name


class Task(Schedule):
    urgent = models.IntegerField(choices=URGENT)
    completed = models.BooleanField()

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=64)


class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    time = models.DateTimeField(default=now)
    created = models.DateTimeField(auto_now_add=True)
