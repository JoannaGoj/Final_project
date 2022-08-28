from datetime import datetime

from freezegun import freeze_time
import pytest
from django.urls import reverse

# Create your tests here.


def test_login_view_get(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200

@freeze_time("Jan 14th, 2012")
@pytest.mark.django_db
def test_login_view_post_correct(client, user_login):
    today = datetime.now()
    year = today.year
    month = today.month
    day = today.day
    url = reverse('login')
    response = client.post(url, user_login)
    assert response.status_code == 302
    assert response.url == reverse('daily_planner', kwargs={'year':year, 'month':month, 'day':day})
    assert year == 2012


def test_login_view_post_incorrect(client):
    url = reverse('login')
    response = client.post(url)
    assert response.status_code == 200


def test_register_get(client):
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_register_post(client):
    url = reverse('register')
    data = {
        'username': 'username',
        'password': 'testowy',
        'password2': 'testowy',

    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_register_post_incorrect(client):
    url = reverse('register')
    data = {
        'username': 'username',
        'password': 'testowy',
        'password2': 'testincorrect',

    }
    response = client.post(url, data)
    assert response.status_code == 200


def test_logout_get(client):
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

