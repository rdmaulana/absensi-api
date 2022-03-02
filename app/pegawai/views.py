import uuid, os
from werkzeug.utils import secure_filename
from flask import Blueprint, jsonify, request
from app.auth.helper import token_required
from app.models import (
    JenisKelamin, 
    Departemen, 
    UnitKerja, 
    Pendidikan,
    Jabatan,
    User,
    BaseModel
)
from app.pegawai.helper import (
    response,
    response_get_json_list,
    response_created_jkelamin, 
    response_created_departemen,
    response_created_unit_kerja,
    response_created_pendidikan,
    response_created_jabatan,
    response_created_pegawai,
    response_updated_pegawai
)
from app.config import allowed_file_upload
from app.config import BaseConfig
from app.pegawai.schema import (
    employees_schema, 
    employees_hrd_schema
)

pegawai = Blueprint('pegawai', __name__)
settings = BaseConfig()

@pegawai.route("/combo/jenis-kelamin/", methods=["GET"])
@token_required
def get_list_jkel(current_user):
    list = []
    data = JenisKelamin.get_all()

    for obj in data:
        list.append(obj.json())
    return response_get_json_list(list)

@pegawai.route("/jenis-kelamin/", methods=["POST"])
@token_required
def create_jkel(current_user):
    if request.content_type == 'application/json':
        data = request.get_json()
        jkel = data.get('namaJenisKelamin')
        if jkel:
            jkel_dt = JenisKelamin(jkel)
            jkel_dt.save()
            return response_created_jkelamin(jkel_dt, 201)
        return response('gagal', 'Missing attribute namaJenisKelamin', 400)
    return response('Failed', 'Content type must be json', 202)

@pegawai.route("/combo/departemen/", methods=["GET"])
@token_required
def get_list_departemen(current_user):
    list = []
    data = Departemen.get_all()

    for obj in data:
        list.append(obj.json())
    return response_get_json_list(list)

@pegawai.route("/departemen/", methods=["POST"])
@token_required
def create_departemen(current_user):
    if request.content_type == 'application/json':
        data = request.get_json()
        departement = data.get('namaDepartemen')
        if departement:
            departement_dt = Departemen(departement)
            departement_dt.save()
            return response_created_departemen(departement_dt, 201)
        return response('Failed', 'Missing attribute namaDepartemen', 400)
    return response('Failed', 'Content type must be json', 202)

@pegawai.route("/combo/unit-kerja/", methods=["GET"])
@token_required
def get_list_unit_kerja(current_user):
    list = []
    data = UnitKerja.get_all()

    for obj in data:
        list.append(obj.json())
    return response_get_json_list(list)

@pegawai.route("/unit-kerja/", methods=["POST"])
@token_required
def create_unit_kerja(current_user):
    if request.content_type == 'application/json':
        data = request.get_json()
        unit_kerja = data.get('namaUnitKerja')
        if unit_kerja:
            unit_kerja_dt = UnitKerja(unit_kerja)
            unit_kerja_dt.save()
            return response_created_unit_kerja(unit_kerja_dt, 201)
        return response('Failed', 'Missing attribute namaUnitKerja', 400)
    return response('Failed', 'Content type must be json', 202)

@pegawai.route("/combo/pendidikan/", methods=["GET"])
@token_required
def get_list_pendidikan(current_user):
    list = []
    data = Pendidikan.get_all()

    for obj in data:
        list.append(obj.json())
    return response_get_json_list(list)

@pegawai.route("/pendidikan/", methods=["POST"])
@token_required
def create_pendidikan(current_user):
    if request.content_type == 'application/json':
        data = request.get_json()
        pendidikan = data.get('namaPendidikan')
        if pendidikan:
            pendidikan_dt = Pendidikan(pendidikan)
            pendidikan_dt.save()
            return response_created_pendidikan(pendidikan_dt, 201)
        return response('Failed', 'Missing attribute namaPendidikan', 400)
    return response('Failed', 'Content type must be json', 202)

@pegawai.route("/combo/jabatan/", methods=["GET"])
@token_required
def get_list_jabatan(current_user):
    list = []
    data = Jabatan.get_all()

    for obj in data:
        list.append(obj.json())
    return response_get_json_list(list)

@pegawai.route("/jabatan/", methods=["POST"])
@token_required
def create_jabatan(current_user):
    if request.content_type == 'application/json':
        data = request.get_json()
        jabatan = data.get('namaJabatan')
        if jabatan:
            jabatan_dt = Jabatan(jabatan)
            jabatan_dt.save()
            return response_created_jabatan(jabatan_dt, 201)
        return response('Failed', 'Missing attribute namaJabatan', 400)
    return response('Failed', 'Content type must be json', 202)

@pegawai.route("/combo/departemen-hrd/", methods=["GET"])
@token_required
def get_list_pegawai_hrd(current_user):
    data = User.get_pegawai_hrd(current_user.namaPerusahaan)
    result = employees_hrd_schema.dump(data)
    return response_get_json_list(result)

@pegawai.route("/daftar/", methods=["GET"])
@token_required
def get_list_pegawai(current_user):
    if User.is_admin_or_hr(current_user.id):
        employees = User.get_all_pegawai(current_user.namaPerusahaan)
        result = employees_schema.dump(employees)

        return response_get_json_list(result)
    return response("gagal", 'Akses ditolak', 401)

@pegawai.route("/admin-tambah-pegawai/", methods=["POST"])
@token_required
def create_pegawai(current_user):
    if request.content_type == 'application/json':
        if User.is_admin_or_hr(current_user.id):
            data = request.get_json()

            nama = data.get('namaLengkap') 
            email = data.get('email') 
            tempat_lahir= data.get('tempatLahir') 
            tanggal_lahir= data.get('tanggalLahir')
            nik_user = data.get('nikUser')
            kd_jk= data.get('kdJenisKelamin')
            nama_jk = JenisKelamin.get_by_id(kd_jk).namaJenisKelamin
            kd_pendidikan = data.get('kdPendidikan')
            nama_pendidikan = Pendidikan.get_by_id(kd_pendidikan).namaPendidikan
            kd_jabatan= data.get('kdJabatan')
            nama_jabatan = Jabatan.get_by_id(kd_jabatan).namaJabatan
            kd_departemen= data.get('kdDepartemen')
            nama_departemen = Departemen.get_by_id(kd_jabatan).namaDepartemen
            kd_unit_kerja= data.get('kdUnitKerja')
            nama_unit_kerja = UnitKerja.get_by_id(kd_unit_kerja).namaUnitKerja
            password = data.get('password')
            password_confirm = data.get('passwordC')
            profile = 'pegawai_perusahaan'
            perusahaan = current_user.namaPerusahaan 

            if data:
                if not password == password_confirm:
                    return response('gagal', 'Password tidak sesuai', 400)
                pegawai_dt = User(
                    nama=nama, 
                    email=email, 
                    tempat_lahir=tempat_lahir, 
                    tanggal_lahir=tanggal_lahir, 
                    nik_user=nik_user,
                    kd_jk=kd_jk,
                    nama_jk=nama_jk,
                    kd_pendidikan=kd_pendidikan,
                    nama_pendidikan=nama_pendidikan,
                    kd_jabatan=kd_jabatan,
                    nama_jabatan=nama_jabatan,
                    kd_departemen=kd_departemen,
                    nama_departemen=nama_departemen,
                    kd_unit_kerja=kd_unit_kerja,
                    nama_unit_kerja=nama_unit_kerja,
                    password=password,
                    profile=profile,
                    perusahaan=perusahaan
                )
                pegawai_dt.save_pegawai()
                return response_created_pegawai("Sukses menambah data pegawai", 201)
            return response('gagal', 'Missing required attribute', 400)
        return response("gagal", 'Akses ditolak', 401)  
    return response('gagal', 'Content type must be json', 202)

@pegawai.route("/admin-ubah-pegawai/", methods=["POST"])
@token_required
def edit_pegawai(current_user):
    if request.content_type == 'application/json':
        if User.is_admin_or_hr(current_user.id):
            data = request.get_json()
            try:
                id_user = data.get('idUser')
                current_pegawai = User.get_by_id(int(id_user))
            except Exception:
                return response('gagal', 'Harap masukkan ID Pegawai yang benar', 400)

            if current_pegawai:
                if data.get('namaLengkap'):
                    current_pegawai.namaLengkap = data['namaLengkap']
                if data.get('email'):
                    current_pegawai.email = data['email']
                if data.get('tempatLahir'):
                    current_pegawai.tempatLahir = data['tempatLahir']
                if data.get('tanggalLahir'):
                    current_pegawai.tanggalLahir = data['tanggalLahir']
                if data.get('nikUser'):
                    current_pegawai.nikUser = data['nikUser']
                if data.get('kdJenisKelamin'):
                    current_pegawai.kdJenisKelamin = data['kdJenisKelamin']
                    current_pegawai.namaJenisKelamin = JenisKelamin.get_by_id(data['kdJenisKelamin']).namaJenisKelamin
                if data.get('kdPendidikan'):
                    current_pegawai.kdPendidikan = data['kdPendidikan']
                    current_pegawai.namaPendidikan = Pendidikan.get_by_id(data['kdPendidikan']).namaPendidikan
                if data.get('kdJabatan'):
                    current_pegawai.kdJabatan = data['kdJabatan']
                    current_pegawai.namaJabatan = Jabatan.get_by_id(data['kdJabatan']).namaJabatan
                if data.get('kdDepartemen'):
                    current_pegawai.kdDepartemen = data['kdDepartemen']
                    current_pegawai.namaDepartemen = Departemen.get_by_id(data['kdDepartemen']).namaDepartemen
                if data.get('kdUnitKerja'):
                    current_pegawai.kdUnitKerja = data['kdUnitKerja']
                    current_pegawai.namaUnitKerja = UnitKerja.get_by_id(data['kdUnitKerja']).namaUnitKerja
                if data.get('password'):
                    if not data['password'] == data['passwordC']:
                        return response('gagal', 'Password tidak sesuai', 400)
                    from app import bcrypt
                    current_pegawai.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
                if current_user:
                    User.update_pegawai(current_pegawai)
                return response_updated_pegawai("Sukses update data pegawai", 201)
            return response('gagal', 'Pegawai dengan id ' + id_user + ' tidak ditemukan', 404)
        return response("gagal", 'Akses ditolak', 401)   
    return response('failed', 'Content-type must be json', 401)

@pegawai.route("/admin-ubah-photo", methods=["POST"])
@token_required
def update_admin_photo(current_user):
    if User.is_admin_or_hr(current_user.id):
        try:
            id_user = request.form.get('idUser')
            judul = request.form.get('namaFile')
            current_pegawai = User.get_by_id(int(id_user))

            if 'files' not in request.files:
                return response('gagal', 'File tidak tersedia', 400)
            
            file = request.files['files']
            if file and allowed_file_upload(file.filename):
                uid = uuid.uuid4()
                filename = secure_filename(file.filename)
                rename_file = f"upload-{uid}-{filename}"
                
                file.save(os.path.join(settings.UPLOAD_FOLDER, rename_file))
                current_pegawai.photo = rename_file
                User.update_pegawai(current_pegawai)
                return response_updated_pegawai("Sukses update foto profil pegawai", 201)
            return response('gagal', 'Ekstensi file tidak di izinkan', 400)
        except Exception as e:
            return e
    return response("gagal", 'Akses ditolak', 401)

@pegawai.route("/ubah-photo", methods=["POST"])
@token_required
def update_pegawai_photo(current_user):
    try:
        judul = request.form.get('namaFile')
        current_pegawai = User.get_by_id(current_user.id)

        if 'files' not in request.files:
            return response('gagal', 'File tidak tersedia', 400)
        
        file = request.files['files']
        if file and allowed_file_upload(file.filename):
            uid = uuid.uuid4()
            filename = secure_filename(file.filename)
            rename_file = f"upload-{uid}-{filename}"
            
            file.save(os.path.join(settings.UPLOAD_FOLDER, rename_file))
            current_pegawai.photo = rename_file
            User.update_pegawai(current_pegawai)
            return response_updated_pegawai("Sukses update foto profil", 201)
        return response('gagal', 'Ekstensi file tidak di izinkan', 400)
    except Exception as e:
        return e

