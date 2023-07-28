import pytest
from rest_framework import status

from user.models import User
from rest_framework.test import APIClient


client = APIClient()


@pytest.fixture
def create_user():
    def _create_user(username, password):
        return User.objects.create_user(username=username, password=password)

    return _create_user


@pytest.mark.django_db
def test_user_str_method():
    user = User(username="test_user")
    assert str(user) == "test_user"


@pytest.mark.django_db
def test_create_user(client):
    # "создание пользователя"
    url = "/user/"
    data = {
        "username": "test_user",
        "password": "test_password",
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert User.objects.get().username == "test_user"


@pytest.mark.django_db
def test_get_user_list(client, create_user):
    # "получение списка пользователей"
    user1 = create_user(username="user1", password="user1_password")
    user2 = create_user(username="user2", password="user2_password")

    url = "/user/"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["username"] == user1.username
    assert response.data[1]["username"] == user2.username


@pytest.mark.django_db
def test_user_authentication(client, create_user):
    # "аутентификация пользователя"
    user = create_user(username="test_user", password="test_password")

    url = "/token/login/"
    data = {"username": "test_user", "password": "test_password"}

    response = client.post(url, data, format="json")

    assert user
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_create_user_with_invalid_data(client):
    # "создание пользователя с ложными данными"
    url = "/user/"
    data = {"username": "", "password": ""}

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data
    assert "password" in response.data
