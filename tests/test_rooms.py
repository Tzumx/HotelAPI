# import asyncio
import pytest
from fastapi.testclient import TestClient

roomtype_len = 0
room_len = 0


@pytest.fixture
def client(client: TestClient):
    '''Update global variable'''

    global roomtype_len, room_len
    roomtype_len = len(client.get('/roomtype').json())
    room_len = len(client.get('/room').json())
    yield client


def test_roomtype_create(client):
    '''Test creation and getting room's types'''

    request_data = {
        'type': 'super-puper',
        'price': 999.9,
        'description': 'Best room',
        'is_doublebad': True,
        'is_bathroom': True,
        'is_conditioner': True,
        'is_TV': True,
    }
    response = client.post('/roomtype', json=request_data)
    assert response.status_code == 200
    new_id = int(response.json()['id'])
    assert response.json()['type'] == 'super-puper'
    assert response.json()['price'] == 999.9
    assert response.json()['description'] == 'Best room'
    assert response.json()['is_doublebad'] == True
    assert response.json()['is_bathroom'] == True
    assert response.json()['is_kitchen'] == False

    response = client.get('/roomtype')
    assert len(response.json()) == roomtype_len+1
    assert response.json()[roomtype_len+0]['type'] == 'super-puper'

    request_data = {
        'type': 'Single',
        'price': 99.9,
        'description': 'Simple room',
        'is_conditioner': True,
    }
    response = client.post('/roomtype', json=request_data)
    assert response.status_code == 200
    assert response.json()['id'] == new_id+1
    assert response.json()['type'] == 'Single'
    assert response.json()['price'] == 99.9
    assert response.json()['description'] == 'Simple room'
    assert response.json()['is_conditioner'] == True

    response = client.get('/roomtype')
    assert len(response.json()) == roomtype_len+2
    assert response.json()[roomtype_len+1]['price'] == 99.9

    request_data = {
        'type': 'Double',
        'price': "error",
        'description': 'Double room',
    }
    response = client.post('/roomtype', json=request_data)
    assert response.status_code == 422

    response = client.get('/roomtype')
    assert len(response.json()) == roomtype_len+2


def test_room_create(client: TestClient):
    '''Test creation and getting rooms'''

    request_data = {
        'type': 'Double',
        'price': 199.9,
        'description': 'Simple room',
        'is_conditioner': True,
    }
    response = client.post('/roomtype', json=request_data)
    assert response.status_code == 200

    roomtype_id = response.json()['id']
    request_data = {
        'number': 4444,
        'type_id': roomtype_id,
        'is_clean': True,
    }
    response = client.post('/room', json=request_data)
    assert response.status_code == 200
    new_id = int(response.json()['id'])
    assert response.json()['number'] == 4444
    assert response.json()['type_id'] == roomtype_id
    assert response.json()['is_clean'] == True

    response = client.get('/room')
    assert len(response.json()) == 1
    assert response.json()[room_len+0]['number'] == 4444

    request_data = {
        'number': 8888,
        'type_id': roomtype_id,
        'is_clean': False,
    }
    response = client.post('/room', json=request_data)
    assert response.status_code == 200
    assert response.json()['id'] == new_id+1
    assert response.json()['number'] == 8888
    assert response.json()['type_id'] == roomtype_id
    assert response.json()['is_clean'] == False

    response = client.get('/room')
    assert len(response.json()) == room_len+2
    assert response.json()[room_len+1]['is_clean'] == False

    request_data = {
        'number': 88888,
        'is_clean': False,
    }
    response = client.post('/room', json=request_data)
    assert response.status_code == 422

    response = client.get('/room')
    assert len(response.json()) == room_len+2


def test_roomtype_delete(client: TestClient):
    """Test delete room's type"""

    request_data = {
        'type': 'Double',
        'price': 199.9,
        'description': 'Simple room',
        'is_conditioner': True,
    }
    response = client.post('/roomtype', json=request_data)
    assert response.status_code == 200
    roomtype_id = response.json()['id']

    request_data = {
        'number': 9999,
        'type_id': roomtype_id,
        'is_clean': True,
    }
    response = client.post('/room', json=request_data)
    assert response.status_code == 200

    response = client.delete(f'/roomtype?id={roomtype_id}')
    assert response.json()['result'] == "Success"

    response = client.get('/room')
    assert len(response.json()) == room_len

    response = client.get('/roomtype')
    assert len(response.json()) == roomtype_len

    response = client.delete(f'/roomtype?id={roomtype_id+1}')
    assert response.json()['result'] == "Error"

    response = client.get('/roomtype')
    assert len(response.json()) == roomtype_len


def test_room_delete(client: TestClient):
    """Test rooms deletion"""

    request_data = {
        'type': 'Double',
        'price': 199.9,
        'description': 'Simple room',
        'is_conditioner': True,
    }
    response = client.post('/roomtype', json=request_data)
    assert response.status_code == 200

    roomtype_id = response.json()['id']
    request_data = {
        'number': 5555,
        'type_id': roomtype_id,
        'is_clean': True,
    }
    response = client.post('/room', json=request_data)
    assert response.status_code == 200
    room_id = response.json()['id']

    response = client.delete(f'/room?id={room_id}')
    assert response.json()['result'] == "Success"

    response = client.delete(f'/room?id={room_id+2}')
    assert response.json()['result'] == "Error"

    response = client.get('/room')
    assert len(response.json()) == room_len
