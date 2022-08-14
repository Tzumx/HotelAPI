import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
import datetime
from utils import users as users_utils
from schemas import guests as guests_schema, requests as requests_schema
from pydantic import ValidationError


guest_1_data = {
    'name': 'name_of_guest',
    'email': 'name@guest.com',
    'phone': '1234567890',
}
guest_2_data = {
    'name': 'name_of_guest2',
    'email': 'nam2e@guest.com',
    'phone': '98746543210',
}


@pytest.fixture
def client_no_auth(client: TestClient):
    '''Update global variable'''

    # skips the authentication
    def skip_auth():
        pass
    app.dependency_overrides[users_utils.get_current_user] = skip_auth

    yield client


def test_routers_guest_create(client_no_auth):
    """Test routers endpoints for create guests"""

    with patch('crud.guests.create_guest') as mock:
        mock.return_value = guests_schema.GuestInfo(
            **(guest_1_data | {"id": 11}))
        response = client_no_auth.post('/guests', json=guest_1_data)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == 11
        assert data['name'] == 'name_of_guest'

        response = client_no_auth.post('/guests', json={})
        assert response.status_code == 422

        try:
            mock.return_value = guests_schema.GuestDeleteInfo(
                **{"status": "ok"})
            response = client_no_auth.post('/guests', json=guest_1_data)
        except ValidationError:
            assert True

        try:
            mock.return_value = guests_schema.GuestInfo(**{"status": "ok"})
        except ValidationError:
            assert True


def test_routers_guest_filter(client_no_auth):
    """Test routers endpoints for filter guests"""

    with patch('crud.guests.filter_guests') as mock:
        mock.return_value = [guests_schema.GuestInfo(**(guest_1_data | {"id": 11})),
                             guests_schema.GuestInfo(**(guest_2_data | {"id": 11}))]
        response = client_no_auth.post('/guests/filter', json={})
        assert response.status_code == 200
        data = response.json()
        assert data[0]['id'] == 11
        assert data[1]['name'] == guest_2_data['name']

        try:
            mock.return_value = guests_schema.GuestDeleteInfo(
                **{"status": "ok"})
            response = client_no_auth.post('/guests/filter', json=guest_1_data)
        except ValidationError:
            assert True


def test_routers_guest_update(client_no_auth):
    """Test routers endpoints for guests update"""

    with patch('crud.guests.update_guest') as mock:
        mock.return_value = guests_schema.GuestInfo(
            **(guest_1_data | {"id": 11}))
        response = client_no_auth.put('/guests/1', json={})
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == guest_1_data['name']

        try:
            mock.return_value = guests_schema.GuestDeleteInfo(
                **{"status": "ok"})
            response = client_no_auth.put('/guests/1', json=guest_1_data)
        except ValidationError:
            assert True


def test_routers_guest_delete(client_no_auth):
    """Test routers endpoints for delete guests"""

    with patch('crud.guests.delete_guest') as mock:
        mock.return_value = {"result": "success"}
        response = client_no_auth.delete('/guests/1')
        assert response.status_code == 200
        data = response.json()
        assert data['result'] == 'success'

        try:
            mock.return_value = guests_schema.GuestDeleteInfo(
                **{"status": "ok"})
            response = client_no_auth.delete('/guests/1', json=guest_1_data)
        except ValidationError:
            assert True


def test_routers_guest(client_no_auth):
    """Test routers endpoints for guests's requests"""

    with patch('crud.guests.get_guest_requests') as mock:
        mock.return_value = [requests_schema.RequestInfo(**{"id": 1, "booking_id": 1,
                                                            "is_closed": True, "price": 100, "description": "descr",
                                                            "updated_at": datetime.datetime.now(), "created_at": datetime.datetime.now()})]
        response = client_no_auth.get('/guests/1/requests')
        assert response.status_code == 200
        data = response.json()
        assert data[0]['booking_id'] == 1

        try:
            mock.return_value = guests_schema.GuestDeleteInfo(
                **{"status": "ok"})
            response = client_no_auth.get(
                '/guests/1/requests', json=guest_1_data)
        except ValidationError:
            assert True


def test_crud_guests_correct(client_no_auth):
    """ Test crud via endpoints """

    response = client_no_auth.post('/guests', json=guest_1_data)
    assert response.status_code == 200
    assert response.json()['email'] == guest_1_data['email']
    id_guest_1 = response.json()['id']

    response = client_no_auth.put(
        f'/guests/{id_guest_1}', json={'phone': "9876543210"})
    assert response.status_code == 200
    response = client_no_auth.post(
        '/guests/filter', json={'phone': "9876543210"})
    data = response.json()
    right_item = False
    for item in data:
        if item['id'] == id_guest_1:
            assert item['phone'] == "9876543210"
            assert item['name'] == guest_1_data['name']
            right_item = True
    assert right_item

    response = client_no_auth.delete(f'/guests/{id_guest_1}')
    assert response.status_code == 200
    response = client_no_auth.post(
        '/guests/filter', json={'phone': "9876543210"})
    data = response.json()
    right_item = True
    for item in data:
        if item['id'] == id_guest_1:
            right_item = False
    assert right_item

    response = client_no_auth.delete(f'/guests/{id_guest_1+888}')
    assert response.status_code == 404


def test_crud_guests_wrong(client_no_auth):
    """ Test mistakes crud via endpoints """

    response = client_no_auth.post('/guests', json={"status": "ok"})
    assert response.status_code == 422

    response = client_no_auth.put(
        f'/guests/-1', json={'phone': "9876543210"})
    assert response.status_code == 404

    response = client_no_auth.delete(f'/guests/-1')
    assert response.status_code == 404
