import json, pytest

def test_adding_jenis_kelamin(test_client, user_token):
    response = test_client.post(
        '/api/pegawai/jenis-kelamin/',
        data = json.dumps(
            dict(
                namaJenisKelamin = "Perempuan"
            )
        ),
        headers = dict(
            Authorization = 'Bearer ' + user_token
        ),
        content_type = 'application/json'
    )
    data = json.loads(response.data.decode())
    assert response.content_type == 'application/json'
    assert response.status_code == 201
    
    assert data['kdJenisKelamin']
    assert data['namaJenisKelamin'] == 'Perempuan'
    assert data['status'] == 'success'

def test_getting_jenis_kelamin(test_client, user_token):
    response = test_client.get(
        '/api/pegawai/combo/jenis-kelamin/',
        headers = dict(
            Authorization = 'Bearer ' + user_token
        )
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data != None

def test_adding_departemen(test_client, user_token):
    response = test_client.post(
        '/api/pegawai/departemen/',
        data = json.dumps(
            dict(
                namaDepartemen = "HRD"
            )
        ),
        headers = dict(
            Authorization = 'Bearer ' + user_token
        ),
        content_type = 'application/json'
    )
    data = json.loads(response.data.decode())
    assert response.content_type == 'application/json'
    assert response.status_code == 201
    
    assert data['kdDepartemen'] 
    assert data['namaDepartemen'] == 'HRD'
    assert data['status'] == 'success'

def test_getting_departemen(test_client, user_token):
    response = test_client.get(
        '/api/pegawai/combo/departemen/',
        headers = dict(
            Authorization = 'Bearer ' + user_token
        )
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data != None

def test_adding_jabatan(test_client, user_token):
    response = test_client.post(
        '/api/pegawai/jabatan/',
        data = json.dumps(
            dict(
                namaJabatan = "Product Designer"
            )
        ),
        headers = dict(
            Authorization = 'Bearer ' + user_token
        ),
        content_type = 'application/json'
    )
    data = json.loads(response.data.decode())
    assert response.content_type == 'application/json'
    assert response.status_code == 201
    
    assert data['kdJabatan'] 
    assert data['namaJabatan'] == 'Product Designer'
    assert data['status'] == 'success'

def test_getting_jabatan(test_client, user_token):
    response = test_client.get(
        '/api/pegawai/combo/jabatan/',
        headers = dict(
            Authorization = 'Bearer ' + user_token
        )
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data != None

def test_adding_pendidikan(test_client, user_token):
    response = test_client.post(
        '/api/pegawai/pendidikan/',
        data = json.dumps(
            dict(
                namaPendidikan = "S1"
            )
        ),
        headers = dict(
            Authorization = 'Bearer ' + user_token
        ),
        content_type = 'application/json'
    )
    data = json.loads(response.data.decode())
    assert response.content_type == 'application/json'
    assert response.status_code == 201
    
    assert data['kdPendidikan']
    assert data['namaPendidikan'] == 'S1'
    assert data['status'] == 'success'

def test_getting_pendidikan(test_client, user_token):
    response = test_client.get(
        '/api/pegawai/combo/pendidikan/',
        headers = dict(
            Authorization = 'Bearer ' + user_token
        )
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data != None

def test_adding_unit_kerja(test_client, user_token):
    response = test_client.post(
        '/api/pegawai/unit-kerja/',
        data = json.dumps(
            dict(
                namaUnitKerja = "Sistem Informasi"
            )
        ),
        headers = dict(
            Authorization = 'Bearer ' + user_token
        ),
        content_type = 'application/json'
    )
    data = json.loads(response.data.decode())
    assert response.content_type == 'application/json'
    assert response.status_code == 201

    assert data['kdUnitKerja']
    assert data['namaUnitKerja'] == 'Sistem Informasi'
    assert data['status'] == 'success'

def test_getting_unit_kerja(test_client, user_token):
    response = test_client.get(
        '/api/pegawai/combo/unit-kerja/',
        headers = dict(
            Authorization = 'Bearer ' + user_token
        )
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data != None

def test_get_list_departemen_hrd(test_client, user_token):
    response = test_client.get(
        '/api/pegawai/combo/departemen-hrd/',
        headers = dict(
            Authorization = 'Bearer ' + user_token
        )
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 200
    assert data != None