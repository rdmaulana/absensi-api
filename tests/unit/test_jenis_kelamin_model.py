from app.models import JenisKelamin

def test_create_jkel():
    jkel = JenisKelamin(
        namaJenisKelamin='Laki-laki'
    )

    assert jkel.namaJenisKelamin == 'Laki-laki'

def test_get_jkel(init_database):
    jkel = JenisKelamin.get_by_id(id=1)

    assert jkel.namaJenisKelamin == 'Laki-laki'