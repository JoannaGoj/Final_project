from django.utils import timezone

def date_time_today(request):
    today = timezone.now().date()
    date = {
        'year': today.year,
        'month': today.month,
        'day': today.day}
    return date