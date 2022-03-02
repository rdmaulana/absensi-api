from app.models import Departemen

def test_create_departemen():
    departemen = Departemen(
        namaDepartemen='HRD'
    )

    assert departemen.namaDepartemen == 'HRD'
    assert type(departemen.namaDepartemen) == str