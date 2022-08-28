from datetime import datetime

import pytest
from django.urls import reverse
from freezegun import freeze_time

from planner.models import Task


# Create your tests here.



@pytest.mark.django_db
def test_redirect_not_logged_in(client):
    url = reverse('redirect_to_daily_planner')
    response = client.get(url)
    assert response.status_code == 302

@freeze_time("Jan 14th, 2012")
@pytest.mark.django_db
def test_redirect_login(client, user):
    url = reverse('redirect_to_daily_planner')
    client.force_login(user)
    response = client.get(url)
    today = datetime.now()
    assert response.status_code == 302
    assert response.url == reverse('daily_planner', args=(today.year, today.month, today.day, ))
    assert today.day == 14

@pytest.mark.django_db
def test_manage_tasks_get_not_logged_in(client):
    url = reverse('manage_tasks')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_manage_tasks_get_login(client, user):
    url = reverse('manage_tasks')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_manage_tasks_post_login_incorrect_form(client, user):
    url = reverse('manage_tasks')
    data = {
        'name': 'name',
        'description': 'description',
        'user': user.id,
    }
    response = client.post(url, data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_manage_events_get_not_logged_in(client):
    url = reverse('manageevents')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_manage_events_get_login(client, user):
    url = reverse('manageevents')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_manage_tags_get_not_logged_in(client):
    url = reverse('manage_tags')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_manage_tags_get_login(client, user):
    url = reverse('manage_tags')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_show_journal_get_not_logged_in(client):
    url = reverse('show_all_journal_entries')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_show_journal_get_login(client, user):
    url = reverse('show_all_journal_entries')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@freeze_time("Jan 14th, 2012")
def test_daily_planner_not_logged_in(client):
    today = datetime.now()
    url = reverse('daily_planner', args=(today.year, today.month, today.day))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))
    assert today.year == 2012

@pytest.mark.django_db
@freeze_time("Jan 14th, 2012")
def test_daily_planner_get_login(client, user):
    today = datetime.now()
    url = reverse('daily_planner', args=(today.year, today.month, today.day))
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    assert today.month == 1


@pytest.mark.django_db
def test_update_event_get_not_logged_in(client, event):
    url = reverse('update_event', args=(event.id,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))
@pytest.mark.django_db
def test_update_event_get_login(client, user, event):
    url = reverse('update_event', args=(event.id,))
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_event_update_post(client, user, event):
    url = reverse('update_event', args=(event.id,))
    today = datetime.now()
    data = {
        'user': user.id,
        'name': 'testowy',
        'description': 'testowy',
        'start_time': today,
        'end_time': today,
        'urgent': '1',
        'completed': False,

    }
    client.force_login(user)
    response = client.post(url, data)
    assert response.status_code == 302

@pytest.mark.django_db
def test_update_tag_get_not_logged_in(client, tag):
    url = reverse('update_tag', args=(tag.id,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))
@pytest.mark.django_db
def test_update_tag_get_login(client, user, tag):
    url = reverse('update_tag', args=(tag.id,))
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_tag_update_post(client, user, tag):
    url = reverse('update_tag',  args=(tag.id,))
    client.force_login(user)
    data = {
        'name':'tagnameupdate'
    }
    response = client.post(url, data)
    assert response.status_code == 302

@pytest.mark.django_db
def test_update_journal_get_not_logged_in(client, journal):
    url = reverse('update_journal_entry', args=(journal.id,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))
@pytest.mark.django_db
def test_update_journal_get_login(client, user, journal):
    url = reverse('update_journal_entry', args=(journal.id,))
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_journal_update_post(client, user, journal):
    url = reverse('update_journal_entry',  args=(journal.id,))
    data = {
        'name':'journalnameupdate'
    }
    response = client.post(url, data)
    assert response.status_code == 302

@pytest.mark.django_db
def test_update_task_get_not_logged_in(client, task):
    url = reverse('update_task', args=(task.id,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))
@pytest.mark.django_db
def test_update_tasks_get_login(client, user, task):
    url = reverse('update_task', args=(task.id,))
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_task_update_post(client, user, task):
    url = reverse('update_task',  args=(task.id,))
    data = {
        'name':'tasknameupdate'
    }
    response = client.post(url, data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_event_get_not_logged_in(client, event):
    url = reverse('delete_event', args=(event.id,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_delete_event_get_login(client, user, event):
    url = reverse('delete_event', args=(event.id,))
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_event_post(client, user, event):
    client.force_login(user)
    url = reverse('delete_event', args=(event.id,))
    data = {
        'pk':event.id
    }
    response = client.post(url, data)
    assert response.status_code == 302

@pytest.mark.django_db
def test_delete_task_get_not_logged_in(client, task):
    url = reverse('delete_task', args=(task.id,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_delete_task_get_login(client, user, task):
    url = reverse('delete_task', args=(task.id,))
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_task_post(client, user, task):
    client.force_login(user)
    url = reverse('delete_task', args=(task.id,))
    data = {
        'pk':task.id
    }
    response = client.post(url, data)
    assert response.status_code == 302



@pytest.mark.django_db
def test_delete_journal_get_not_logged_in(client, journal):
    url = reverse('delete_journal_entry', args=(journal.id,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_delete_journal_get_login(client, user, journal):
    url = reverse('delete_journal_entry', args=(journal.id,))
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_task_post(client, user, journal):
    client.force_login(user)
    url = reverse('delete_journal_entry', args=(journal.id,))
    data = {
        'pk':journal.id
    }
    response = client.post(url, data)
    assert response.status_code == 302

@pytest.mark.django_db
def test_delete_tag_get_not_logged_in(client, tag):
    url = reverse('delete_tag', args=(tag.id,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_delete_tag_get_login(client, user, tag):
    url = reverse('delete_tag', args=(tag.id,))
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_tag_post(client, user, tag):
    client.force_login(user)
    url = reverse('delete_tag', args=(tag.id,))
    data = {
        'pk':tag.id
    }
    response = client.post(url, data)
    assert response.status_code == 302




