import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
import datetime
from utils import users as users_utils
from schemas import payments as payments_schema
from pydantic import ValidationError

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


def test_routers_payments_create(client_no_auth):
    """Test routers endpoints for payments create"""

    with patch('crud.payments.create_payment') as mock:
        mock.return_value = payments_schema.PaymentInfo(
            **(payment_data | {"id": 11}))
        response = client_no_auth.post('/payments', json=payment_data)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == 11
        assert data['description'] == payment_data['description']

        response = client_no_auth.post('/payments', json={})
        assert response.status_code == 422

        try:
            mock.return_value = payments_schema.PaymentDeleteInfo(**{"status": "ok"})
            response = client_no_auth.post('/payments', json=payment_data)
        except ValidationError:
            assert True

        try:
            mock.return_value = payments_schema.PaymentInfo(**{"status": "ok"})
        except ValidationError:
            assert True     

def test_routers_payments_filter(client_no_auth):
    """Test routers endpoints for payments filter"""

    with patch('crud.payments.filter_payments') as mock:
        mock.return_value = [payments_schema.PaymentInfo(
            **(payment_data | {"id": 11})), ]
        response = client_no_auth.post('/payments/filter', json={})
        assert response.status_code == 200
        data = response.json()
        assert data[0]['sum'] == payment_data['sum']

        try:
            mock.return_value = payments_schema.PaymentDeleteInfo(**{"status": "ok"})
            response = client_no_auth.post('/payments/filter', json=payment_data)
        except ValidationError:
            assert True        

def test_routers_payments_update(client_no_auth):
    """Test routers endpoints for payments update"""

    with patch('crud.payments.update_payment') as mock:
        mock.return_value = payments_schema.PaymentInfo(
            **(payment_data | {"sum": 33, "id": 11}))
        response = client_no_auth.put('/payments/11', json={"sum": 33})
        assert response.status_code == 200
        data = response.json()
        assert data['sum'] == 33

        try:
            mock.return_value = payments_schema.PaymentDeleteInfo(**{"status": "ok"})
            response = client_no_auth.post('/payments/11', json=payment_data)
        except ValidationError:
            assert True           

def test_routers_payments_delete(client_no_auth):
    """Test routers endpoints for payments delete"""

    with patch('crud.payments.delete_payment') as mock:
        mock.return_value = {"result": "success"}
        response = client_no_auth.delete('/payments/11')
        assert response.status_code == 200
        data = response.json()
        assert data['result'] == 'success'

        try:
            mock.return_value = payments_schema.PaymentDeleteInfo(
                **{"status": "ok"})
            response = client_no_auth.delete('/payments/11', json=payment_data)
        except ValidationError:
            assert True

def test_crud_payments_correct(client_no_auth):
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
    data = response.json()
    payment_id = data['id']
    assert data['sum'] == payment_data['sum']
    assert data['booking_id'] == booking_id  

    response = client_no_auth.put(f'/payments/{payment_id}', json={'sum': 33})
    assert response.status_code == 200
    response = client_no_auth.post('/payments/filter', json={'sum': 33})
    data = response.json()
    right_item = False
    for item in data:
        if item['id'] == payment_id:
            assert item['sum'] == 33
            right_item = True
    assert right_item

    response = client_no_auth.delete(f'/payments/{payment_id}')
    assert response.status_code == 200
    response = client_no_auth.post('/payments/filter')
    data = response.json()
    right_item = True
    for item in data:
        if item['id'] == payment_id:
            right_item = False
    assert right_item

    response = client_no_auth.delete(f'/payments/{payment_id+888}')
    assert response.status_code == 404


def test_crud_payments_wrong(client_no_auth):
    """ Test crud with mistakes via endpoints """

    response = client_no_auth.post('/payments', json=booking_data)
    assert response.status_code == 422 

    response = client_no_auth.put(f'/payments/-1', json={'sum': 33})
    assert response.status_code == 404

    response = client_no_auth.delete(f'/payments/-1')
    assert response.status_code == 404
