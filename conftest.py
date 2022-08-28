from datetime import datetime

from django.contrib.auth.models import User, Permission
import pytest

from freezegun import freeze_time
from planner.models import Task, Tags, Journal, Event


@pytest.fixture
def user_login():
    data = {
        'username': 'usernamelogintest',
        'password': 'usernamepasslogintest'
    }
    User.objects.create_user(**data)
    return data

@pytest.fixture
def user_register():
    data = {
        'username': 'usernametest',
        'password': 'passtest',
        'password2':'passtest'
    }
    return User.objects.create_user(**data)


@pytest.fixture
def user():
    data = {
        'username': 'usernametest',
        'password': 'usernamepasstest',
        'pk': '1'

    }
    return User.objects.create_user(**data)

@pytest.fixture
def tag():
    t = Tags.objects.create(name='tagnametest', pk=1)
    return t

@pytest.fixture
def task(user):
    t = Task.objects.create(name="taskname", user=user)
    return t

@pytest.fixture
def journal(user):
    j = Journal.objects.create(name="journalname", user=user)
    return j

@pytest.fixture
def event(user):
    e = Event.objects.create(name="eventname", user=user)
    return e



@freeze_time("Jan 14th, 2012")
@pytest.fixture
def tasks_list(user):
    for x in range(10):
        lst = []
        t = Task()
        t.user = user
        t.name = 'taskname'+ str(x)
        t.save()
        lst.append(t)
        return lst


@pytest.fixture
@freeze_time("Jan 14th, 2012")
def today():
    today = datetime.now()
    return today
