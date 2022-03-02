import json

from app.models import BaseModel

def test_checkin_absen(test_client, user_token_pegawai):
    response = test_client.get(
        '/api/presensi/in',
        headers = dict(
            Authorization = 'Bearer '+ user_token_pegawai
        )
    )
    data = json.loads(response.data.decode())
    
    print(response)
    assert response.status_code == 201
    assert data['jamMasuk'] == BaseModel.generate_datetime_to_epoc()
    assert type(data['jamMasuk']) == int

def test_checkin_absen_already(test_client, user_token_pegawai):
    response = test_client.get(
        '/api/presensi/in',
        headers = dict(
            Authorization = 'Bearer '+ user_token_pegawai
        )
    )
    data = json.loads(response.data.decode())
    
    assert response.status_code == 400
    assert data['status'] == 'gagal'
    assert data['message'] == 'Anda sudah melakukan absen hari ini'

def test_checkout_absen(test_client, user_token_pegawai):
    response = test_client.get(
        '/api/presensi/out',
        headers = dict(
            Authorization = 'Bearer '+ user_token_pegawai
        )
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 201
    assert data['jamKeluar'] == BaseModel.generate_datetime_to_epoc()
    assert type(data['jamKeluar']) == int

def test_history_absensi_pegawai(test_client, user_token_pegawai):
    tgl_awal = BaseModel.generate_epoc_date()
    tgl_akhir = BaseModel.generate_epoc_date()
    response = test_client.get(
        f'/api/presensi/daftar/pegawai?tglAwal={tgl_awal}&tglAkhir={tgl_akhir}',
        headers = dict(
            Authorization = 'Bearer '+ user_token_pegawai
        )
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 200
    assert type(data) == list
    assert len(data) != 0

def test_history_absensi_pegawai_notvalid(test_client, user_token_pegawai):
    tgl_awal = BaseModel.generate_epoc_date()
    response = test_client.get(
        f'/api/presensi/daftar/pegawai?tglAwal={tgl_awal}&tglAkhir=',
        headers = dict(
            Authorization = 'Bearer '+ user_token_pegawai
        )
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert data['status'] == 'gagal'
    assert data['message'] == 'Atribut form tidak lengkap'

def test_get_combo_status_absen(test_client, user_token_pegawai):
    response = test_client.get(
        '/api/presensi/combo/status-absen',
        headers = dict(
            Authorization = 'Bearer ' + user_token_pegawai
        )
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert type(data) == list
    assert len(data) != 0
    
def test_get_history_absensi_pegawai_all(test_client, user_token):
    tgl_awal = BaseModel.generate_epoc_date()
    tgl_akhir = BaseModel.generate_epoc_date()

    response = test_client.get(
        '/api/presensi/daftar/admin?tglAwal={0}&tglAkhir={1}'.format(tgl_awal, tgl_akhir),
        headers = dict(
            Authorization = 'Bearer ' + user_token
        )
    )
    print(response)
    data = json.loads(response.data.decode())

    assert response.status_code == 200
    assert type(data) == list
    assert len(data) != 0

def test_history_absensi_pegawai_all_notvalid(test_client, user_token):
    tgl_awal = BaseModel.generate_epoc_date()
    response = test_client.get(
        f'/api/presensi/daftar/admin?tglAwal={tgl_awal}&tglAkhir=',
        headers = dict(
            Authorization = 'Bearer '+ user_token
        )
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert data['status'] == 'gagal'
    assert data['message'] == 'Atribut paramater tidak lengkap'

def test_history_absensi_pegawai_all_unauthorized(test_client, user_token_pegawai):
    tgl_awal = BaseModel.generate_epoc_date()
    tgl_akhir = BaseModel.generate_epoc_date()
    
    response = test_client.get(
        '/api/presensi/daftar/admin?tglAawal={0}&tglAkhir={1}'.format(tgl_awal, tgl_akhir),
        headers = dict(
            Authorization = 'Bearer '+ user_token_pegawai
        )
    )
    data = json.loads(response.data.decode()) 

    assert response.status_code == 401
    assert response.content_type == 'application/json'

    assert data['status'] == 'gagal'
    assert data['message'] == 'Akses ditolak'

def test_create_absensi(test_client, user_token_pegawai):
    response = test_client.post(
        '/api/presensi/absensi',
        headers = dict(
            Authorization = 'Bearer '+ user_token_pegawai
        ),
        data = json.dumps(
            dict(
                tglAbsensi = BaseModel.generate_epoc_date(),
                kdStatus = 2
            )
        ),
        content_type = 'application/json'
    )
    data = json.loads(response.data.decode())
    print(response)

    assert response.status_code == 201
    assert response.content_type == 'application/json'
    assert data['status'] == 'sukses'
    assert data['message'] == 'Berhasil menyimpan absensi'

def test_create_absensi_failed(test_client, user_token_pegawai):
    response = test_client.post(
        '/api/presensi/absensi',
        headers = dict(
            Authorization = 'Bearer '+ user_token_pegawai
        ),
        data = json.dumps(
            dict(
                tglAbsensi = BaseModel.generate_epoc_date(),
            )
        ),
        content_type = 'application/json'
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert data['status'] == 'gagal'
    assert data['message'] == 'Atribut form tidak lengkap'

