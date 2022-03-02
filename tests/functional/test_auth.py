import json
import pytest

def test_user_init_data(test_client, register_user):
    data = json.loads(register_user.data.decode())

    assert register_user.content_type == 'application/json'
    assert register_user.status_code == 201
    assert data['email'] == 'adrian_arnold@demo.com'
    assert data['password'] 
    assert data['profile'] == 'admin_perusahaan'

def test_missing_attribute_init_data(test_client, init_database):
    response = test_client.post(
        '/api/auth/init-data',
        content_type='application/json',
        data = json.dumps(
            dict(
                namaAdmin='Adrian Arnold', 
                perusahaan=None
            )
        )
    )
    data = json.loads(response.data.decode())

    assert response.content_type == 'application/json'
    assert response.status_code == 400
    assert data['status']  == 'failed'
    assert data['message'] == 'Missing attribute namaAdmin or perusahaan'

def test_email_already_exist_init_data(test_client, register_user):
    exist_user = json.loads(register_user.data.decode())
    response = test_client.post(
        '/api/auth/init-data',
        content_type='application/json',
        data = json.dumps(
            dict(
                namaAdmin='Adrian Arnold', 
                perusahaan='PT. Teknologi Basah'
            )
        )
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert data['status']  == 'failed'
    assert data['message'] == 'Failed, User already exists, Please sign In'