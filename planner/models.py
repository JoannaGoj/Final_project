from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from ckeditor.fields import RichTextField

# Create your models here.


URGENT = (
    (1, 'max priority'),
    (2, 'urgent'),
    (3, 'not urgent'),

)


# musze pousuwac start time i endtime ze schedule i przeniesc to do eventow tylko
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
        how_many_days_to_task = (date.today() - self.start_time.date()).days
        if how_many_days_to_task < 0:
            is_past_or_approaching += 'Already past'
            return is_past_or_approaching, how_many_days_to_task
        elif 0 <= how_many_days_to_task < 3:
            is_past_or_approaching += 'Soon approaching!'
            return is_past_or_approaching, how_many_days_to_task
        else:
            is_past_or_approaching += 'In future'
            return is_past_or_approaching, how_many_days_to_task

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

    def related_tags(self):
        tags = Tags.objects.all()
        return tags


# usunac additional notes to jest tymczasowe
class Event(Schedule):
    additional_note = models.CharField(max_length=50)


def class_id(self):
    return "event"


class Task(Schedule):
    urgent = models.IntegerField(choices=URGENT, default=2)
    completed = models.BooleanField(default=False)

    def class_id(self):
        return 'task'


class Tags(models.Model):
    name = models.CharField(max_length=64)
    color = models.CharField(default="#E6C3CD", max_length=7, blank=True)

    def related_schedules(self):
        related_schedules = Schedule.objects.all()
        return related_schedules


class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60, blank=True)
    text = RichTextField(blank=True, null=True)
    date_of_entry = models.DateTimeField(auto_now_add=True)

    def class_id(self):
        return "journal"
