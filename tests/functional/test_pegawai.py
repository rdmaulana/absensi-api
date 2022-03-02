import json
import io

def test_get_list_pegawai(test_client, user_token):
    response = test_client.get(
        '/api/pegawai/daftar/',
        headers = dict(
            Authorization = 'Bearer ' + user_token
        )
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert type(data) == list
    assert len(data) != 0

def test_get_list_pegawai_unauthorized(test_client, user_token_pegawai):
    response = test_client.get(
        '/api/pegawai/daftar/',
        headers = dict(
            Authorization = 'Bearer ' + user_token_pegawai
        )
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 401
    assert response.content_type == 'application/json'
    assert data['status'] == 'gagal'
    assert data['message'] == 'Akses ditolak'

def test_create_pegawai(test_client, user_token):
    response = test_client.post(
        '/api/pegawai/admin-tambah-pegawai/',
        headers = dict(
            Authorization = 'Bearer '+ user_token
        ),
        data = json.dumps(
            dict(
                namaLengkap = 'Adrian Arnold',
                email = 'adrian_arnold@mail.com',
                tempatLahir = 'Manado',
                tanggalLahir = 856371600,
                nikUser = '3271050897890011',
                kdJenisKelamin = 1,
                kdPendidikan = 1,
                kdJabatan = 1,
                kdDepartemen = 1,
                kdUnitKerja = 1,
                password = 'qweasdzxc',
                passwordC = 'qweasdzxc',
            )
        ),
        content_type = 'application/json'
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 201
    assert data['message'] == 'Sukses menambah data pegawai'
    assert data['status'] == 'sukses'

def test_create_pegawai_unauthorized(test_client, user_token_pegawai):
    response = test_client.post(
        '/api/pegawai/admin-tambah-pegawai/',
        headers = dict(
            Authorization = 'Bearer '+ user_token_pegawai
        ),
        data = json.dumps(
            dict(
                namaLengkap = 'Adrian Arnold',
                email = 'adrian_arnold@mail.com',
                tempatLahir = 'Manado',
                tanggalLahir = 856371600,
                nikUser = '3271050897890011',
                kdJenisKelamin = 2,
                kdPendidikan = 1,
                kdJabatan = 1,
                kdDepartemen = 1,
                kdUnitKerja = 1,
                password = 'qweasdzxc',
                passwordC = 'qweasdzxc',
            )
        ),
        content_type = 'application/json'
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 401
    assert data['message'] == 'Akses ditolak'
    assert data['status'] == 'gagal'

def test_edit_pegawai(test_client, user_token):
    response = test_client.post(
        '/api/pegawai/admin-ubah-pegawai/',
        headers = dict(
            Authorization = 'Bearer '+ user_token
        ),
        data = json.dumps(
            dict(
                idUser = '2',
                namaLengkap = 'Adrian Arnold Imanuel',
                tempatLahir = 'Kota Manado',
            )
        ),
        content_type = 'application/json'
    )
    data = json.loads(response.data.decode()) 

    assert response.status_code == 201
    assert response.content_type == 'application/json'

    assert data['status'] == 'sukses'
    assert data['message'] == 'Sukses update data pegawai'

def test_edit_pegawai_id_pegawai_badformat(test_client, user_token):
    response = test_client.post(
        '/api/pegawai/admin-ubah-pegawai/',
        headers = dict(
            Authorization = 'Bearer '+ user_token
        ),
        data = json.dumps(
            dict(
                idUser = '73biuds8',
                namaLengkap = 'Adrian Arnold Imanuel',
                tempatLahir = 'Kota Manado',
            )
        ),
        content_type = 'application/json'
    )
    data = json.loads(response.data.decode()) 

    assert response.status_code == 400
    assert response.content_type == 'application/json'

    assert data['status'] == 'gagal'
    assert data['message'] == 'Harap masukkan ID Pegawai yang benar'

def test_edit_pegawai_id_pegawai_notfound(test_client, user_token):
    response = test_client.post(
        '/api/pegawai/admin-ubah-pegawai/',
        headers = dict(
            Authorization = 'Bearer '+ user_token
        ),
        data = json.dumps(
            dict(
                idUser = '255555',
                namaLengkap = 'Adrian Arnold Imanuel',
                tempatLahir = 'Kota Manado',
            )
        ),
        content_type = 'application/json'
    )
    data = json.loads(response.data.decode()) 

    assert response.status_code == 404
    assert response.content_type == 'application/json'

    assert data['status'] == 'gagal'
    assert data['message'] == 'Pegawai dengan id 255555 tidak ditemukan'

def test_edit_pegawai_unauthorized(test_client, user_token_pegawai):
    response = test_client.post(
        '/api/pegawai/admin-ubah-pegawai/',
        headers = dict(
            Authorization = 'Bearer '+ user_token_pegawai
        ),
        data = json.dumps(
            dict(
                idUser = '2',
                namaLengkap = 'Adrian Arnold Imanuel',
                tempatLahir = 'Kota Manado',
            )
        ),
        content_type = 'application/json'
    )
    data = json.loads(response.data.decode()) 

    assert response.status_code == 401
    assert response.content_type == 'application/json'

    assert data['status'] == 'gagal'
    assert data['message'] == 'Akses ditolak'

def test_uodate_admin_photo(test_client, user_token):
    import io

    data = dict(
        idUser = '1',
        namaFile = 'foto profile'
    )
    data['files'] = (io.BytesIO(b"tests/img_sample/663219154.png"), '663219154.png')
    
    response = test_client.post(
        '/api/pegawai/admin-ubah-photo',
        headers = dict(
            Authorization = 'Bearer '+ user_token
        ),
        data = data,
        content_type = 'multipart/form-data'
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 201
    assert data['status'] == 'sukses'
    assert data['message'] == 'Sukses update foto profil pegawai'

def test_update_admin_photo_files_not_found(test_client, user_token):
    response = test_client.post(
        '/api/pegawai/admin-ubah-photo',
        headers = dict(
            Authorization = 'Bearer '+ user_token
        ),
        data = dict(
            idUser = '1',
            namaFile = 'foto profile'
        ),
        content_type = 'multipart/form-data'
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert data['status'] == 'gagal'
    assert data['message'] == 'File tidak tersedia'

def test_update_admin_photo_file_extension_notvalid(test_client, user_token):
    data = dict(
        idUser = '1',
        namaFile = 'foto profile'
    )
    data['files'] = (io.BytesIO(b"tests/img_sample/663219154.gif"), '663219154.gif')
    
    response = test_client.post(
        '/api/pegawai/admin-ubah-photo',
        headers = dict(
            Authorization = 'Bearer '+ user_token
        ),
        data = data,
        content_type = 'multipart/form-data'
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert data['status'] == 'gagal'
    assert data['message'] == 'Ekstensi file tidak di izinkan'

def test_update_admin_photo_unauthorized(test_client, user_token_pegawai):
    data = dict(
        idUser = '1',
        namaFile = 'foto profile'
    )
    data['files'] = (io.BytesIO(b"tests/img_sample/663219154.png"), '663219154.png')
    
    response = test_client.post(
        '/api/pegawai/admin-ubah-photo',
        headers = dict(
            Authorization = 'Bearer '+ user_token_pegawai
        ),
        data = data,
        content_type = 'multipart/form-data'
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 401
    assert data['status'] == 'gagal'
    assert data['message'] == 'Akses ditolak'

def test_update_pegawai_photo(test_client, user_token_pegawai):
    data = dict(
        namaFile = 'foto profil'
    )
    data['files'] = (io.BytesIO(b"tests/img_sample/663219154.png"), '663219154.png')
    
    response = test_client.post(
        '/api/pegawai/ubah-photo',
        headers = dict(
            Authorization = 'Bearer ' + user_token_pegawai
        ),
        data = data,
        content_type = 'multipart/form-data'
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 201
    assert data['status'] == 'sukses'
    assert data['message'] == 'Sukses update foto profil'

def test_update_admin_photo_files_not_found(test_client, user_token_pegawai):
    response = test_client.post(
        '/api/pegawai/ubah-photo',
        headers = dict(
            Authorization = 'Bearer '+ user_token_pegawai
        ),
        data = dict(
            namaFile = 'foto profil'
        ),
        content_type = 'multipart/form-data'
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert data['status'] == 'gagal'
    assert data['message'] == 'File tidak tersedia'

def test_update_pegawai_photo_file_extension_notvalid(test_client, user_token_pegawai):
    data = dict(
        namaFile = 'foto profile'
    )
    data['files'] = (io.BytesIO(b"tests/img_sample/663219154.gif"), '663219154.gif')
    
    response = test_client.post(
        '/api/pegawai/ubah-photo',
        headers = dict(
            Authorization = 'Bearer '+ user_token_pegawai
        ),
        data = data,
        content_type = 'multipart/form-data'
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert data['status'] == 'gagal'
    assert data['message'] == 'Ekstensi file tidak di izinkan'
