from app.models import User

def test_new_user():
    user = User(
        email='rdmaulana01@gmail.com', 
        password='qweasdzxc', 
        profile='admin_perusahaan', 
        nama='Raden Maulana', 
        perusahaan='PT. Kayo Teknologi', 
    )
    assert user.email == 'rdmaulana01@gmail.com'
    assert user.password != 'qweasdzxc'
    assert user.profile == 'admin_perusahaan'
    assert user.namaLengkap == 'Raden Maulana'
    assert user.namaPerusahaan == 'PT. Kayo Teknologi'

def test_get_user_by_id_with_fixture(init_database):
    user = User.get_by_id(user_id=1)

    assert user.email == 'rdmaulana01@gmail.com'
    assert user.password != 'qweasdzxc'
    assert user.profile == 'admin_perusahaan'
    assert user.namaLengkap == 'Raden Maulana'
    assert user.namaPerusahaan == 'PT. Kayo Teknologi'

def test_get_user_by_email_with_fixture(init_database):
    user = User.get_by_email(email='rdmaulana01@gmail.com')

    assert user.email == 'rdmaulana01@gmail.com'
    assert user.password != 'qweasdzxc'
    assert user.profile == 'admin_perusahaan'
    assert user.namaLengkap == 'Raden Maulana'
    assert user.namaPerusahaan == 'PT. Kayo Teknologi'

def test_check_user_is_admin_or_hr(init_database):
    user = User.is_admin_or_hr(user_id=1)
    assert user