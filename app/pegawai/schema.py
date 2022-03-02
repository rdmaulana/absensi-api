from app import ma 
from app.models import (
    Absensi,
    User
)

class EmployeeSchema(ma.Schema):
    class Meta:
        fields = (
            'profile',
            'idUser',
            'namaLengkap',
            'tempatLahir',
            'tanggalLahir',
            'email',
            'password',
            'nikUser',
            'kdJabatan',
            'namaJabatan',
            'kdDepartemen',
            'namaDepartemen',
            'kdUnitKerja',
            'namaJenisKelamin',
            'kdPendidikan',
            'namaPendidikan',
            'namaPendidikan',
            'photo'
        )

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

class EmployeeHRDSchema(ma.Schema):
    class Meta:
        fields = (
            'namaLengkap',
            'kdJabatan',
            'namaJabatan'
        )

employees_hrd_schema = EmployeeHRDSchema(many=True)