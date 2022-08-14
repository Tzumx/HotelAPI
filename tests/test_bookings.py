import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
import datetime
from utils import users as users_utils
from schemas import bookings as bookings_schema


booking_data = {
    'room_number': 1,
    'guest_id': 1,
    'check_in': str(datetime.datetime.now() - datetime.timedelta(hours=1)),
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
def client(client: TestClient):
    '''Update global variable'''

    # skips the authentication
    def skip_auth():
        pass
    app.dependency_overrides[users_utils.get_current_user] = skip_auth

    yield client


def test_routers_bookings(client):
    """Test routers endpoints for bookings"""

    booking_data_2 = booking_data.copy()
    booking_data_2['room_number'] = 2
    booking_data_add_2 = booking_data_add.copy()
    booking_data_add_2['id'] = 22
    booking_data_add_2['client_review'] = "2nd review"

    with patch('crud.bookings.create_booking') as mock:
        mock.return_value = bookings_schema.BookingInfo(
            **(booking_data | booking_data_add))
        response = client.post('/bookings', json=booking_data)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == booking_data_add['id']
        assert data['description'] == booking_data['description']

    with patch('crud.bookings.filter_bookings') as mock:
        mock.return_value = [bookings_schema.BookingInfo(**(booking_data | booking_data_add)),
                             bookings_schema.BookingInfo(**(booking_data_2 | booking_data_add_2))]
        response = client.post('/bookings/filter', json={})
        assert response.status_code == 200
        data = response.json()
        assert data[0]['id'] == booking_data_add['id']
        assert data[1]['client_review'] == '2nd review'

    with patch('crud.bookings.update_booking') as mock:
        mock.return_value = bookings_schema.BookingInfo(
            **(booking_data | booking_data_add_2))
        response = client.put('/bookings/1', json={})
        assert response.status_code == 200
        data = response.json()
        assert data['client_review'] == booking_data_add_2['client_review']

    with patch('crud.bookings.delete_booking') as mock:
        mock.return_value = {"result": "success"}
        response = client.delete('/bookings/11')
        assert response.status_code == 200
        data = response.json()
        assert data['result'] == 'success'

    with patch('crud.bookings.set_booking_status') as mock:
        mock.return_value = bookings_schema.BookingInfo(
            **(booking_data | booking_data_add))
        response = client.patch('/bookings/11/is_active?is_active=True')
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == booking_data_add['id']


def test_crud_bookings(client):
    """ Test crud via endpoints """

    # create supporting data
    response = client.post('/guests', json=guest_data)
    assert response.status_code == 200
    id_guest = response.json()['id']

    response = client.post('/roomtypes', json=roomtype_data)
    assert response.status_code == 200
    roomtype_id = response.json()['id']

    room_data = {
        'number': 4444,
        'room_types_id': roomtype_id,
        'floor': 1,
        'housing': 2,
    }
    response = client.post('/rooms', json=room_data)
    assert response.status_code == 200

    booking_data['guest_id'] = id_guest
    booking_data['room_number'] = room_data['number']

    response = client.post('/bookings', json=booking_data)
    assert response.status_code == 200
    data = response.json()
    booking_id = data['id']
    assert data['room_number'] == room_data['number']
    assert data['description'] == booking_data['description']

    # can not add booking if room is busy
    response = client.post('/bookings', json=booking_data)
    assert response.status_code == 409

    booking_data['check_in'] = str(datetime.datetime.now() - \
        datetime.timedelta(days=5))
    booking_data['check_out'] = str(datetime.datetime.now() + \
        datetime.timedelta(days=5))
    response = client.post('/bookings', json=booking_data)
    assert response.status_code == 409

    booking_data['check_in'] = str(datetime.datetime.now() + \
        datetime.timedelta(days=5))
    booking_data['check_out'] = str(datetime.datetime.now() + \
        datetime.timedelta(days=15))
    response = client.post('/bookings', json=booking_data)
    assert response.status_code == 409

    booking_data['check_in'] = str(datetime.datetime.now() - \
        datetime.timedelta(days=5))
    booking_data['check_out'] = str(datetime.datetime.now() + \
        datetime.timedelta(days=15))
    response = client.post('/bookings', json=booking_data)
    assert response.status_code == 409

    booking_data['check_in'] = str(datetime.datetime.now() + \
        datetime.timedelta(days=2))
    booking_data['check_out'] = str(datetime.datetime.now() + \
        datetime.timedelta(days=4))
    response = client.post('/bookings', json=booking_data)
    assert response.status_code == 409

    booking_data['check_in'] = str(datetime.datetime.now() + \
        datetime.timedelta(days=15))
    booking_data['check_out'] = str(datetime.datetime.now() + \
        datetime.timedelta(days=25))
    response = client.post('/bookings', json=booking_data)
    assert response.status_code == 200

    response = client.put(
        f'/bookings/{booking_id}', json={'description': "desc_of_booking_2"})
    assert response.status_code == 200
    response = client.post(
        '/bookings/filter', json={'description': "desc_of_booking_2"})
    data = response.json()
    right_item = False
    for item in data:
        if item['id'] == booking_id:
            assert item['description'] == "desc_of_booking_2"
            assert item['guest_id'] == id_guest
            right_item = True
    assert right_item


    response = client.get(f'/rooms/{room_data["number"]}/guests')
    assert response.status_code == 200
    assert response.json()[0]["name"] == guest_data["name"]


    response = client.patch(
        f'/bookings/{booking_id}/is_active?is_active=False')
    assert response.status_code == 200
    response = client.patch(
        f'/bookings/{booking_id}/review', json={"review": "client_review"})
    assert response.status_code == 200
    response = client.post(
        '/bookings/filter', json={'description': "desc_of_booking_2"})
    data = response.json()
    for item in data:
        if item['id'] == booking_id:
            assert item['is_active'] == False
            assert item['client_review'] == "client_review"

    response = client.get(f'/bookings/{booking_id}/sum')
    assert response.status_code == 200
    assert response.json()['sum'] == roomtype_data['price']

    response = client.delete(f'/bookings/{booking_id}')
    assert response.status_code == 200
    response = client.post(
        '/bookings/filter', json={'description': "desc_of_booking_2"})
    data = response.json()
    right_item = True
    for item in data:
        if item['id'] == booking_id:
            right_item = False
    assert right_item

    response = client.delete(f'/bookings/{booking_id+888}')
    assert response.status_code == 404
