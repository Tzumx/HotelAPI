import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
from utils import users as users_utils
from schemas import users as users_schema

user_data = {
    "email": "test@user.com",
    "name": "user_test",
    "password": "strong_password",
    "is_active": True,
    "is_admin": True,
}


@pytest.fixture
def client(client: TestClient):
    '''Update global variable'''

    # skips the authentication
    def skip_auth():
        pass
    app.dependency_overrides[users_utils.get_current_user] = skip_auth
    app.dependency_overrides[users_utils.get_admin_user] = skip_auth

    yield client


def test_routers_users(client):
    """Test routers endpoints for users"""

    with patch('crud.users.create_user') as mock:
        mock.return_value = users_schema.UserInfo(
            **(user_data | {"id": 11}))
        response = client.post('/sign-up', json=user_data)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == 11
        assert data['email'] == user_data['email']

    with patch('crud.users.filter_users') as mock:
        mock.return_value = [users_schema.UserInfo(
            **(user_data | {"id": 11})), ]
        response = client.post('/users/filter', json={})
        assert response.status_code == 200
        data = response.json()
        assert data[0]['email'] == user_data['email']

    with patch('crud.users.update_user') as mock:
        mock.return_value = users_schema.UserInfo(
            **(user_data | {"email": "mail@user.com", "id": 11}))
        response = client.put('/users/11', json={"email": "mail@user.com"})
        assert response.status_code == 200
        data = response.json()
        assert data['email'] == "mail@user.com"

    with patch('crud.users.delete_user') as mock:
        mock.return_value = {"result": "success"}
        response = client.delete('/users/11')
        assert response.status_code == 200
        data = response.json()
        assert data['result'] == 'success'


def test_crud_requests(client):
    """ Test crud via endpoints """

    response = client.post('/sign-up', json=user_data)
    assert response.status_code == 200
    user_id = response.json()['id']
    assert response.json()["name"] == user_data["name"]

    response = client.post('/sign-up', json=user_data)
    assert response.status_code == 400    

    response = client.put(f'/users/{user_id}', json={'name': "new_name"})
    assert response.status_code == 200
    response = client.post('/users/filter', json={'name': "new_name"})
    data = response.json()
    right_item = False
    for item in data:
        if item['id'] == user_id:
            assert item['name'] == "new_name"
            right_item = True
    assert right_item

    response = client.delete(f'/users/{user_id}')
    assert response.status_code == 200
    response = client.post('/users/filter')
    data = response.json()
    right_item = True
    for item in data:
        if item['id'] == user_id:
            right_item = False
    assert right_item

    response = client.delete(f'/users/{user_id+888}')
    assert response.status_code == 404
