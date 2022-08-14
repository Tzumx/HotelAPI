import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
import datetime
from utils import users as users_utils
from schemas import requests as requests_schema
from pydantic import ValidationError

request_data = {
    "booking_id": 1,
    "is_closed": False,
    "description": "requsts's description",
    "price": 11,
    "updated_at": str(datetime.datetime.now()),
    "created_at": str(datetime.datetime.now())
}

payment_data = {
    "sum": 22,
    "date": str(datetime.datetime.now()),
    "booking_id": 1,
    "description": "desc_of_paym",
}

booking_data = {
    'room_number': 1,
    'guest_id': 1,
    'check_in': str(datetime.datetime.now()),
    'check_out': str(datetime.datetime.now() + datetime.timedelta(days=10)),
    'description': "descr of booking",
}
booking_data_add = {
    "id": 11,
    "is_paid": False,
    "is_active": True,
    "client_review": "review",
    "updated_at": datetime.datetime.now(),
    "created_at": datetime.datetime.now(),
}
guest_data = {
    'name': 'name_of_guest',
    'email': 'name@guest.com',
    'phone': '98746543210',
}
roomtype_data = {
    'type_name': 'super-puper',
    'price': 999.9,
    'description': 'Best room',
}


@pytest.fixture
def client_no_auth(client: TestClient):
    '''Update global variable'''

    # skips the authentication
    def skip_auth():
        pass
    app.dependency_overrides[users_utils.get_current_user] = skip_auth

    yield client


def test_routers_requests_create(client_no_auth):
    """Test routers endpoints for requests create"""

    with patch('crud.requests.create_request') as mock:
        mock.return_value = requests_schema.RequestInfo(
            **(request_data | {"id": 11}))
        response = client_no_auth.post('/requests', json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == 11
        assert data['price'] == request_data['price']

        response = client_no_auth.post('/requests', json={})
        assert response.status_code == 422

        with pytest.raises(ValidationError):
            mock.return_value = requests_schema.RequestDeleteInfo(
                **{"status": "ok"})
            response = client_no_auth.post('/requests', json=request_data)

        with pytest.raises(ValidationError):
            mock.return_value = requests_schema.RequestInfo(**{"status": "ok"})


def test_routers_requests_filter(client_no_auth):
    """Test routers endpoints for filter requests"""

    with patch('crud.requests.filter_requests') as mock:
        mock.return_value = [requests_schema.RequestInfo(
            **(request_data | {"id": 11})), ]
        response = client_no_auth.post('/requests/filter', json={})
        assert response.status_code == 200
        data = response.json()
        assert data[0]['price'] == request_data['price']

        with pytest.raises(ValidationError):
            mock.return_value = requests_schema.RequestDeleteInfo(
                **{"status": "ok"})
            response = client_no_auth.post(
                '/requests/filter', json=request_data)


def test_routers_requests_update(client_no_auth):
    """Test routers endpoints for update requests"""

    with patch('crud.requests.update_request') as mock:
        mock.return_value = requests_schema.RequestInfo(
            **(request_data | {"price": 33, "id": 11}))
        response = client_no_auth.put('/requests/11', json={"price": 33})
        assert response.status_code == 200
        data = response.json()
        assert data['price'] == 33

        with pytest.raises(ValidationError):
            mock.return_value = requests_schema.RequestDeleteInfo(
                **{"status": "ok"})
            response = client_no_auth.put('/requests/11', json=request_data)


def test_routers_requests_delete(client_no_auth):
    """Test routers endpoints for delete requests"""

    with patch('crud.requests.delete_request') as mock:
        mock.return_value = {"result": "success"}
        response = client_no_auth.delete('/requests/11')
        assert response.status_code == 200
        data = response.json()
        assert data['result'] == 'success'

        with pytest.raises(ValidationError):
            mock.return_value = requests_schema.RequestDeleteInfo(
                **{"status": "ok"})
            response = client_no_auth.delete('/guests/1', json=request_data)


def test_crud_requests_correct(client_no_auth):
    """ Test crud via endpoints """

    # create supporting data
    response = client_no_auth.post('/guests', json=guest_data)
    assert response.status_code == 200
    id_guest = response.json()['id']

    response = client_no_auth.post('/roomtypes', json=roomtype_data)
    assert response.status_code == 200
    roomtype_id = response.json()['id']

    room_data = {
        'number': 4444,
        'room_types_id': roomtype_id,
        'floor': 1,
        'housing': 2,
    }
    response = client_no_auth.post('/rooms', json=room_data)
    assert response.status_code == 200

    booking_data['guest_id'] = id_guest
    booking_data['room_number'] = room_data['number']

    response = client_no_auth.post('/bookings', json=booking_data)
    assert response.status_code == 200
    booking_id = response.json()['id']

    payment_data['booking_id'] = booking_id
    response = client_no_auth.post('/payments', json=payment_data)
    assert response.status_code == 200

    request_data['booking_id'] = booking_id
    response = client_no_auth.post('/requests', json=request_data)
    assert response.status_code == 200
    data = response.json()
    request_id = data['id']
    assert data['price'] == request_data['price']
    assert data['booking_id'] == booking_id

    response = client_no_auth.get(f'/bookings/{booking_id}/sum')
    assert response.status_code == 200
    assert response.json()['sum'] == roomtype_data['price'] + \
        request_data['price']

    response = client_no_auth.put(
        f'/requests/{request_id}', json={'price': 33})
    assert response.status_code == 200
    response = client_no_auth.post('/requests/filter', json={'price': 33})
    data = response.json()
    right_item = False
    for item in data:
        if item['id'] == request_id:
            assert item['price'] == 33
            right_item = True
    assert right_item

    response = client_no_auth.delete(f'/requests/{request_id}')
    assert response.status_code == 200
    response = client_no_auth.post('/requests/filter')
    data = response.json()
    right_item = True
    for item in data:
        if item['id'] == request_id:
            right_item = False
    assert right_item

    response = client_no_auth.delete(f'/requests/{request_id+888}')
    assert response.status_code == 404


def test_crud_requests_wrong(client_no_auth):
    """ Test crud via endpoints with mistakes """

    response = client_no_auth.post('/requests', json={"status": "ok"})
    assert response.status_code == 422

    response = client_no_auth.put(f'/requests/-1', json={'price': 33})
    assert response.status_code == 404

    response = client_no_auth.delete(f'/requests/-1')
    assert response.status_code == 404
