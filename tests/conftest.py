import pytest
import json
from app import app, db
from app.models import AbsensiStatus, Departemen, Jabatan, Pendidikan, UnitKerja, User, JenisKelamin

@pytest.fixture(scope='module')
def test_client():
    flask_app = app
    flask_app.config.from_object('app.config.TestingConfig')

    with flask_app.test_client() as testing_client:
        yield testing_client

@pytest.fixture(scope='module')
def dummy_master_combo():
    jkel = JenisKelamin(
        namaJenisKelamin='Laki-laki'
    )
    pendidikan = Pendidikan(
        namaPendidikan='D3'
    )
    jabatan = Jabatan(
        namaJabatan='Boss Executive'
    )
    departemen = Departemen(
        namaDepartemen='Sofware Development'
    )
    unit_kerja = UnitKerja(
        namaUnitKerja='QA Tester'
    )
    return jkel, pendidikan, jabatan, departemen, unit_kerja

@pytest.fixture(scope='module')
def dummy_user():
    user_admin = User(
        email='rdmaulana01@gmail.com',
        nama='Raden Maulana',
        password='qweasdzxc',
        profile='admin_perusahaan',
        perusahaan='PT. Kayo Teknologi'
    )
    user_pegawai = User(
        email='pegawai01@gmail.com',
        nama='Marshmallow',
        password='qweasdzxc',
        profile='pegawai_perusahaan',
        perusahaan='PT. Kayo Teknologi'
    )
    return user_admin, user_pegawai

@pytest.fixture(scope='module')
def dummy_status_absen():
    status = AbsensiStatus(
        nama_status='Masuk'
    )
    status_s = AbsensiStatus(
        nama_status='Sakit'
    )
    return status, status_s

@pytest.fixture(scope='module')
def init_database(test_client, dummy_master_combo, dummy_user, dummy_status_absen):
    db.create_all()

    jkel, pendidikan, jabatan, departemen, unit_kerja = dummy_master_combo

    user_admin, user_pegawai = dummy_user

    masuk, sakit = dummy_status_absen

    db.session.add(user_admin)
    db.session.add(user_pegawai)

    db.session.add(jkel)
    db.session.add(pendidikan)
    db.session.add(jabatan)
    db.session.add(departemen)
    db.session.add(unit_kerja)

    db.session.add(masuk)
    db.session.add(sakit)
    
    db.session.commit()

    yield

    db.session.remove()
    db.drop_all()

@pytest.fixture
def register_user(test_client, init_database):
    response = test_client.post(
        '/api/auth/init-data',
        content_type='application/json',
        data = json.dumps(
            dict(
                namaAdmin='Adrian Arnold', 
                perusahaan='PT. Teknologi Basah')
        )
    )
    return response

@pytest.fixture(scope='module')
def user_token(test_client, init_database):
    email = 'rdmaulana01@gmail.com'
    password = 'qweasdzxc'
    profile = 'admin_perusahaan'

    signin = test_client.post(
        '/api/auth/login',
        content_type='application/json',
        data = json.dumps(
            dict(
                email=email, 
                password=password, 
                profile=profile
            )
        )
    )
    return json.loads(signin.data)['hasil']['token']

@pytest.fixture(scope='module')
def user_token_pegawai(test_client, init_database):
    email = 'pegawai01@gmail.com'
    password = 'qweasdzxc'
    profile = 'pegawai_perusahaan'

    signin = test_client.post(
        '/api/auth/login',
        content_type='application/json',
        data = json.dumps(
            dict(
                email=email, 
                password=password, 
                profile=profile
            )
        )
    )
    return json.loads(signin.data)['hasil']['token']

@pytest.fixture(scope='function')
def login_default_user(test_client):
    test_client.post(
        '/api/auth/login',
        data = dict(
            email = 'ajenghanii@gmail.com',
            password = 'qweasdzxc',
            profile = 'admin_perusahaan'
        ),
        follow_redirects=True
    )

    yield

    test_client.post(
        '/api/auth/logout',
        follow_redirects=True
    )