
import pytest
from django.urls import reverse
from freezegun import freeze_time


# Create your tests here.



@pytest.mark.django_db
def test_redirect_not_logged_in(client):
    url = reverse('redirect_to_daily_planner')
    response = client.get(url)
    assert response.status_code == 302

# @freeze_time("Jan 14th, 2012")
# @pytest.mark.django_db
# def test_redirect_login(client, user):
#     url = reverse('redirect_to_daily_planner')
#     client.force_login(user)
#     response = client.get(url)
#     assert response.status_code == 302
#     assert response.url == reverse('daily_planner', args='2012,1,14,')


# ok
@pytest.mark.django_db
def test_show_all_tasks_get_not_logged_in(client):
    url = reverse('manage_tasks')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

# nie działa!!!!!!!!!!!
@pytest.mark.django_db
def test_manage_tasks_get_login(client, user, tasks_list):
    url = reverse('manage_tasks')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200



# NIE DZILAA UWAGA UWAGA UWAGA
@pytest.mark.django_db
def test_manage_tasks_post_login(client, user):
    url = reverse('manage_tasks')
    client.force_login(user)
    tasks_dict = {
        'name': 'taskname',
        'user': user.id
    }
    response = client.post(url, tasks_dict)
    # assert response.status_code == 302
    assert response.url == reverse('manage_tasks')


#OK!!!!!!!!!!!!!!!!!!!!!!!!!      UPDATE      !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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
    url = reverse('update_event',  args=(event.id,))
    data = {
        'user':user,
        'name':'eventnameupdate'
    }
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
    data = {
        'user':user,
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
        'user':user,
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
        'user':user,
        'name':'tasknameupdate'
    }
    response = client.post(url, data)
    assert response.status_code == 302


 #OK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



# !!!!!!!!!!!!!!!!!!!!!!!!!! DELETE !!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
def test_journal_task_post(client, user, journal):
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
def test_journal_tag_post(client, user, tag):
    url = reverse('delete_tag', args=(tag.id,))
    data = {
        'pk':tag.id
    }
    response = client.post(url, data)
    assert response.status_code == 302




