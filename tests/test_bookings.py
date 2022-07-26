import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
import datetime
from utils import users as users_utils
from schemas import bookings as bookings_schema
from pydantic import ValidationError, BytesError

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

booking_data_2 = booking_data.copy()
booking_data_2['room_number'] = 2
booking_data_add_2 = booking_data_add.copy()
booking_data_add_2['id'] = 22
booking_data_add_2['client_review'] = "2nd review"

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


def test_routers_bookings_create(client_no_auth):
    """Test routers endpoints create for bookings"""

    with patch('crud.bookings.create_booking') as mock:
        mock.return_value = bookings_schema.BookingInfo(
            **(booking_data | booking_data_add))
        response = client_no_auth.post('/bookings', json=booking_data)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == booking_data_add['id']
        assert data['description'] == booking_data['description']

        response = client_no_auth.post('/bookings', json=roomtype_data)
        assert response.status_code == 422

        with pytest.raises(ValidationError):
            mock.return_value = bookings_schema.BookingDeleteInfo(
                **{"status": "ok"})
            response = client_no_auth.post('/bookings', json=booking_data)

        with pytest.raises(ValidationError):
            mock.return_value = bookings_schema.BookingInfo(**(roomtype_data))


def test_routers_bookings_filter(client_no_auth):
    """Test routers endpoints filter for bookings"""

    with patch('crud.bookings.filter_bookings') as mock:
        mock.return_value = [bookings_schema.BookingInfo(**(booking_data | booking_data_add)),
                             bookings_schema.BookingInfo(**(booking_data_2 | booking_data_add_2))]
        response = client_no_auth.post('/bookings/filter', json={})
        assert response.status_code == 200
        data = response.json()
        assert data[0]['id'] == booking_data_add['id']
        assert data[1]['client_review'] == '2nd review'

        with pytest.raises(ValidationError):
            mock.return_value = bookings_schema.BookingDeleteInfo(
                **{"status": "ok"})
            response = client_no_auth.post(
                '/bookings/filter', json=booking_data)


def test_routers_bookings_update(client_no_auth):
    """Test routers endpoints update for bookings"""

    with patch('crud.bookings.update_booking') as mock:
        mock.return_value = bookings_schema.BookingInfo(
            **(booking_data | booking_data_add_2))
        response = client_no_auth.put('/bookings/1', json={})
        assert response.status_code == 200
        data = response.json()
        assert data['client_review'] == booking_data_add_2['client_review']

        with pytest.raises(ValidationError):
            mock.return_value = bookings_schema.BookingDeleteInfo(
                **{"status": "ok"})
            response = client_no_auth.put('/bookings/1', json=booking_data)


def test_routers_bookings_delete(client_no_auth):
    """Test routers endpoints delete for bookings"""

    with patch('crud.bookings.delete_booking') as mock:
        mock.return_value = {"result": "success"}
        response = client_no_auth.delete('/bookings/11')
        assert response.status_code == 200
        data = response.json()
        assert data['result'] == 'success'

        with pytest.raises(ValidationError):
            mock.return_value = bookings_schema.BookingInfo(
                **(booking_data | booking_data_add_2))
            response = client_no_auth.delete('/bookings/11', json=booking_data)


def test_routers_bookings_set_status(client_no_auth):
    """Test routers endpoints set status for bookings"""

    with patch('crud.bookings.set_booking_status') as mock:
        mock.return_value = bookings_schema.BookingInfo(
            **(booking_data | booking_data_add))
        response = client_no_auth.patch(
            '/bookings/11/is_active?is_active=True')
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == booking_data_add['id']

        response = client_no_auth.post(
            '/bookings/11/is_active?is_active=Worong')
        assert response.status_code == 405

        with pytest.raises(ValidationError):
            mock.return_value = bookings_schema.BookingDeleteInfo(
                **{"status": "ok"})
            response = client_no_auth.post('/bookings', json=booking_data)


def test_crud_bookings_correct(client_no_auth):
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
    data = response.json()
    booking_id = data['id']
    assert data['room_number'] == room_data['number']
    assert data['description'] == booking_data['description']

    # can not add booking if room is busy
    response = client_no_auth.post('/bookings', json=booking_data)
    assert response.status_code == 409

    booking_data['check_in'] = str(datetime.datetime.now()
                                   - datetime.timedelta(days=5))
    booking_data['check_out'] = str(datetime.datetime.now()
                                    + datetime.timedelta(days=5))
    response = client_no_auth.post('/bookings', json=booking_data)
    assert response.status_code == 409

    booking_data['check_in'] = str(datetime.datetime.now()
                                   + datetime.timedelta(days=5))
    booking_data['check_out'] = str(datetime.datetime.now()
                                    + datetime.timedelta(days=15))
    response = client_no_auth.post('/bookings', json=booking_data)
    assert response.status_code == 409

    booking_data['check_in'] = str(datetime.datetime.now()
                                   - datetime.timedelta(days=5))
    booking_data['check_out'] = str(datetime.datetime.now()
                                    + datetime.timedelta(days=15))
    response = client_no_auth.post('/bookings', json=booking_data)
    assert response.status_code == 409

    booking_data['check_in'] = str(datetime.datetime.now()
                                   + datetime.timedelta(days=2))
    booking_data['check_out'] = str(datetime.datetime.now()
                                    + datetime.timedelta(days=4))
    response = client_no_auth.post('/bookings', json=booking_data)
    assert response.status_code == 409

    booking_data['check_in'] = str(datetime.datetime.now()
                                   + datetime.timedelta(days=15))
    booking_data['check_out'] = str(datetime.datetime.now()
                                    + datetime.timedelta(days=25))
    response = client_no_auth.post('/bookings', json=booking_data)
    assert response.status_code == 200

    response = client_no_auth.put(
        f'/bookings/{booking_id}', json={'description': "desc_of_booking_2"})
    assert response.status_code == 200
    response = client_no_auth.post(
        '/bookings/filter', json={'description': "desc_of_booking_2"})
    data = response.json()
    right_item = False
    for item in data:
        if item['id'] == booking_id:
            assert item['description'] == "desc_of_booking_2"
            assert item['guest_id'] == id_guest
            right_item = True
    assert right_item

    response = client_no_auth.get(f'/rooms/{room_data["number"]}/guests')
    assert response.status_code == 200
    assert response.json()[0]["name"] == guest_data["name"]

    response = client_no_auth.patch(
        f'/bookings/{booking_id}/is_active?is_active=False')
    assert response.status_code == 200
    response = client_no_auth.patch(
        f'/bookings/{booking_id}/review', json={"review": "client_review"})
    assert response.status_code == 200
    response = client_no_auth.post(
        '/bookings/filter', json={'description': "desc_of_booking_2"})
    data = response.json()
    for item in data:
        if item['id'] == booking_id:
            assert item['is_active'] == False
            assert item['client_review'] == "client_review"

    response = client_no_auth.get(f'/bookings/{booking_id}/sum')
    assert response.status_code == 200
    assert response.json()['sum'] == roomtype_data['price']

    response = client_no_auth.delete(f'/bookings/{booking_id}')
    assert response.status_code == 200
    response = client_no_auth.post(
        '/bookings/filter', json={'description': "desc_of_booking_2"})
    data = response.json()
    right_item = True
    for item in data:
        if item['id'] == booking_id:
            right_item = False
    assert right_item

    response = client_no_auth.delete(f'/bookings/{booking_id+888}')
    assert response.status_code == 404


def test_crud_bookings_wrong(client_no_auth):
    """ Test mistakes crud via endpoints """

    response = client_no_auth.post('/bookings', json=guest_data)
    assert response.status_code == 422

    response = client_no_auth.put(
        f'/bookings/-1', json={'description': "desc_of_booking_2"})
    assert response.status_code == 404

    response = client_no_auth.get(f'/rooms/-1/guests')
    assert response.status_code == 404

    response = client_no_auth.patch(
        f'/bookings/-1/is_active?is_active=False')
    assert response.status_code == 404
    response = client_no_auth.patch(
        f'/bookings/-1/review', json={"review": "client_review"})
    assert response.status_code == 404

    response = client_no_auth.get(f'/bookings/-1/sum')
    assert response.status_code == 404

    response = client_no_auth.delete(f'/bookings/-1')
    assert response.status_code == 404
