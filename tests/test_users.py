import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
from utils import users as users_utils
from schemas import users as users_schema
from pydantic import ValidationError

user_data = {
    "email": "test@user.com",
    "name": "user_test",
    "password": "strong_password",
    "is_active": True,
    "is_admin": True,
}


@pytest.fixture
def client_no_auth(client: TestClient):
    '''Update global variable'''

    # skips the authentication
    def skip_auth():
        pass
    app.dependency_overrides[users_utils.get_current_user] = skip_auth
    app.dependency_overrides[users_utils.get_admin_user] = skip_auth

    yield client


def test_routers_users_create(client_no_auth):
    """Test routers endpoints for create users"""

    with patch('crud.users.create_user') as mock:
        mock.return_value = users_schema.UserInfo(
            **(user_data | {"id": 11}))
        response = client_no_auth.post('/sign-up', json=user_data)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == 11
        assert data['email'] == user_data['email']

        response = client_no_auth.post('/guests', json={})
        assert response.status_code == 422

        with pytest.raises(ValidationError):
            mock.return_value = users_schema.UserDeleteInfo(
                **{"status": "ok"})
            response = client_no_auth.post('/sign-up', json=user_data)

        with pytest.raises(ValidationError):
            mock.return_value = users_schema.UserInfo(**{"status": "ok"})


def test_routers_users_filter(client_no_auth):
    """Test routers endpoints for filter users"""

    with patch('crud.users.filter_users') as mock:
        mock.return_value = [users_schema.UserInfo(
            **(user_data | {"id": 11})), ]
        response = client_no_auth.post('/users/filter', json={})
        assert response.status_code == 200
        data = response.json()
        assert data[0]['email'] == user_data['email']

        with pytest.raises(ValidationError):
            mock.return_value = users_schema.UserDeleteInfo(
                **{"status": "ok"})
            response = client_no_auth.post('/users/filter', json=user_data)


def test_routers_users_update(client_no_auth):
    """Test routers endpoints for update users"""

    with patch('crud.users.update_user') as mock:
        mock.return_value = users_schema.UserInfo(
            **(user_data | {"email": "mail@user.com", "id": 11}))
        response = client_no_auth.put(
            '/users/11', json={"email": "mail@user.com"})
        assert response.status_code == 200
        data = response.json()
        assert data['email'] == "mail@user.com"

        with pytest.raises(ValidationError):
            mock.return_value = users_schema.UserDeleteInfo(
                **{"status": "ok"})
            response = client_no_auth.post('/users/-11', json=user_data)


def test_routers_users_delete(client_no_auth):
    """Test routers endpoints for delete users"""

    with patch('crud.users.delete_user') as mock:
        mock.return_value = {"result": "success"}
        response = client_no_auth.delete('/users/11')
        assert response.status_code == 200
        data = response.json()
        assert data['result'] == 'success'

        with pytest.raises(ValidationError):
            mock.return_value = users_schema.UserDeleteInfo(
                **{"status": "ok"})
            response = client_no_auth.post('/users/-11', json=user_data)


def test_crud_requests_correct(client_no_auth):
    """ Test crud via endpoints """

    response = client_no_auth.post('/sign-up', json=user_data)
    assert response.status_code == 200
    user_id = response.json()['id']
    assert response.json()["name"] == user_data["name"]

    response = client_no_auth.post('/sign-up', json=user_data)
    assert response.status_code == 400

    response = client_no_auth.post(
        "/auth", data={"username": user_data["email"], "password": "wrong_password"})
    assert response.status_code == 401

    response = client_no_auth.post(
        "/auth", data={"username": user_data["email"], "password": user_data["password"]})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    refresh_token = data['refresh_token']

    app.dependency_overrides[users_utils.get_admin_user] = users_utils.get_admin_user

    response = client_no_auth.post(
        '/auth/refresh', headers={"authorization": f"Bearer {refresh_token}"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" not in data
    access_token = data['access_token']

    response = client_no_auth.put(f'/users/{user_id}', json={'name': "new_name"},
                                  headers={"authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    response = client_no_auth.post('/users/filter', json={'name': "new_name"}, headers={
        "authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    data = response.json()
    right_item = False
    for item in data:
        if item['id'] == user_id:
            assert item['name'] == "new_name"
            right_item = True
    assert right_item

    response = client_no_auth.post('/users/filter', json={'name': "new_name"}, headers={
        "authorization": f"Bearer wrong_token"})
    assert response.status_code == 403

    response = client_no_auth.delete(
        f'/users/{user_id}', headers={"authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    response = client_no_auth.post(
        '/users/filter', headers={"authorization": f"Bearer {access_token}"})
    data = response.json()
    right_item = True
    for item in data:
        if item['id'] == user_id:
            right_item = False
    assert right_item


def test_crud_requests_wrong(client_no_auth):
    """ Test crud with mistakes via endpoints """

    response = client_no_auth.post('/sign-up', json={})
    assert response.status_code == 422

    response = client_no_auth.post(
        "/auth", data={"username": user_data["email"], "password": "wrong_password"})
    assert response.status_code == 401

    response = client_no_auth.post('/auth/refresh')
    assert response.status_code == 401

    response = client_no_auth.put(f'/users/-1', json={'name': "new_name"})
    assert response.status_code == 404

    response = client_no_auth.delete(f'/users/-888')
    assert response.status_code == 404
