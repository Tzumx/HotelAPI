# import asyncio
import pytest
from fastapi.testclient import TestClient
from typing import Union
from main import app
from utils import users as users_utils

roomtype_len = 0
room_len = 0


@pytest.fixture
def client(client: TestClient):
    '''Update global variable'''

    # skips the authentication
    def skip_auth():
        pass
    app.dependency_overrides[users_utils.get_current_user] = skip_auth

    global roomtype_len, room_len
    roomtype_len = len(client.get('/roomtypes').json())
    room_len = len(client.post('/rooms/filter').json())

    yield client


def test_roomtype_create_update(client):
    '''Test creation and getting room's types'''

    request_data = {
        'type_name': 'super-puper',
        'price': 999.9,
        'description': 'Best room',
    }
    response = client.post('/roomtypes', json=request_data)
    assert response.status_code == 200
    data = response.json()
    new_id = int(data['id'])
    assert data['type_name'] == 'super-puper'
    assert data['price'] == 999.9
    assert data['description'] == 'Best room'

    request_data = {
        'price': 888.9,
    }
    response = client.put(f'/roomtypes/{new_id}', json=request_data)
    assert response.status_code == 200
    assert response.json()['price'] == 888.9

    response = client.get('/roomtypes')
    data = response.json()
    assert len(data) == roomtype_len+1
    assert data[roomtype_len+0]['type_name'] == 'super-puper'

    request_data = {
        'type_name': 'Single',
        'price': 99.9,
    }
    response = client.post('/roomtypes', json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == new_id+1
    assert data['type_name'] == 'Single'
    assert data['price'] == 99.9
    assert data['description'] == None

    response = client.get('/roomtypes')
    data = response.json()
    assert len(data) == roomtype_len+2
    assert data[roomtype_len+1]['price'] == 99.9

    request_data = {
        'type_name': 'Double',
        'price': "error",
        'description': 'Double room',
    }
    response = client.post('/roomtypes', json=request_data)
    assert response.status_code == 422

    response = client.get('/roomtypes')
    assert len(response.json()) == roomtype_len+2


def test_room_create_update(client: TestClient):
    '''Test creation and getting rooms'''

    request_data = {
        'type_name': 'Double',
        'price': 199.9,
        'description': 'Simple room',
    }
    response = client.post('/roomtypes', json=request_data)
    assert response.status_code == 200

    roomtype_id = response.json()['id']
    request_data = {
        'number': 4444,
        'room_types_id': roomtype_id,
        'floor': 1,
        'housing': 2,
    }
    response = client.post('/rooms', json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data['number'] == 4444
    assert data['room_types_id'] == roomtype_id
    assert data['floor'] == 1
    assert data['housing'] == 2

    request_data = {
        'floor': 2,
    }
    response = client.put(f'/rooms/{data["number"]}', json=request_data)
    assert response.status_code == 200
    assert response.json()['floor'] == 2

    response = client.post('/rooms/filter')
    data = response.json()
    assert len(data) == 1
    assert data[room_len+0]['number'] == 4444

    request_data = {
        'number': 8888,
        'room_types_id': roomtype_id,
    }
    response = client.post('/rooms', json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data['number'] == 8888
    assert data['room_types_id'] == roomtype_id

    response = client.post('/rooms', json=request_data)
    assert response.status_code == 409

    response = client.post('/rooms/filter')
    assert len(response.json()) == room_len+2
    assert response.json()[room_len+1]['housing'] == 0

    request_data = {
        'number': 88888,
    }
    response = client.post('/rooms', json=request_data)
    assert response.status_code == 422

    response = client.post('/rooms/filter')
    assert len(response.json()) == room_len+2


def test_roomtype_delete(client: TestClient):
    """Test delete room's type"""

    request_data = {
        'type_name': 'Double',
        'price': 199.9,
        'description': 'Simple room',
    }
    response = client.post('/roomtypes', json=request_data)
    assert response.status_code == 200
    roomtype_id = response.json()['id']

    request_data = {
        'number': 9999,
        'room_types_id': roomtype_id,
    }
    response = client.post('/rooms', json=request_data)
    assert response.status_code == 200

    response = client.delete(f'/roomtypes/{roomtype_id}')
    assert response.json()['result'] == "Success"

    response = client.post('/rooms/filter')
    data = response.json()
    assert len(data) == room_len+1
    data[room_len+0]['room_types_id'] == None

    response = client.get('/roomtypes')
    assert len(response.json()) == roomtype_len

    response = client.delete(f'/roomtypes/{roomtype_id+1}')
    assert response.json()['detail'] == "Not found"

    response = client.get('/roomtypes')
    assert len(response.json()) == roomtype_len


def test_room_delete(client: TestClient):
    """Test rooms deletion"""

    request_data = {
        'type_name': 'Double',
        'price': 199.9,
        'description': 'Simple room',
    }
    response = client.post('/roomtypes', json=request_data)
    assert response.status_code == 200

    roomtype_id = response.json()['id']
    request_data = {
        'number': 5555,
        'room_types_id': roomtype_id,
    }
    response = client.post('/rooms', json=request_data)
    assert response.status_code == 200
    room_number= response.json()['number']

    response = client.delete(f'/rooms/-9')
    assert response.json()['detail'] == "Not found"

    response = client.delete(f'/rooms/{room_number}')
    assert response.json()['result'] == "Success"    

    response = client.post('/rooms/filter')
    assert len(response.json()) == room_len

def test_features(client: TestClient):
    """Test rooms deletion"""

    request_data = {
        'type_name': 'Triple',
        'price': 799.9,
        'description': 'Very big room',
    }
    response = client.post('/roomtypes', json=request_data)
    assert response.status_code == 200
    roomtype_id = response.json()['id']

    request_data = {
        'number': 5656,
        'room_types_id': roomtype_id,
    }
    response = client.post('/rooms', json=request_data)
    assert response.status_code == 200
    room_number= response.json()['number']

    request_data = {
        "feature": "TV"
    }
    response = client.post('/roomtypes/features', json=request_data)
    assert response.status_code == 200
    response.json()['feature'] = "TV"
    feature_id = response.json()['id']

    response = client.post(f'/roomtypes/{roomtype_id}/features?feature_id={feature_id}', json={})
    assert response.status_code == 200
    data = response.json()
    assert data['feature'] == "TV"

    response = client.post('/rooms/filter')
    for elem in response.json():
        if elem['number'] == room_number:
            assert "TV" in elem['features']
