from flask import make_response, jsonify
from app import app, db, bcrypt
import datetime
import jwt
import random
import string

class BaseModel():
    def generate_datetime_to_epoc():
        return int(datetime.datetime.now().timestamp())

    def generate_epoc_to_date():
        return str(datetime.datetime.now().fromtimestamp())

    def generate_epoc_date():
        now = datetime.datetime.now()
        today = now.replace(hour = 0, minute = 0, second = 0)
        return int(today.timestamp())

    def decode_epoc_date(timestamp):
        return str(datetime.datetime.fromtimestamp(timestamp))

class JenisKelamin(db.Model):
    __tablename__ = "tbl_jeniskelamin"
    
    kdJenisKelamin = db.Column(db.Integer, primary_key=True, autoincrement=True)
    namaJenisKelamin = db.Column(db.String(15), nullable=False)

    def __init__(self, namaJenisKelamin):
        self.namaJenisKelamin = namaJenisKelamin

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, namaJenisKelamin):
        self.namaJenisKelamin = namaJenisKelamin
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all():
        return JenisKelamin.query.all()

    def get_by_id(id):
        return JenisKelamin.query.filter_by(kdJenisKelamin=id).first()

    def json(self):
        return {
            'kdJenisKelamin': self.kdJenisKelamin,
            'namaJenisKelamin': self.namaJenisKelamin,
        }
    

class Pendidikan(db.Model):
    __tablename__ = "tbl_pendidikan"

    kdPendidikan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    namaPendidikan = db.Column(db.String(50), nullable=False)

    def __init__(self, namaPendidikan):
        self.namaPendidikan = namaPendidikan

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, namaPendidikan):
        self.namaPendidikan = namaPendidikan
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all():
        return Pendidikan.query.all()

    def get_by_id(id):
        return Pendidikan.query.filter_by(kdPendidikan=id).first()

    def json(self):
        return {
            'kdPendidikan': self.kdPendidikan,
            'namaPendidikan': self.namaPendidikan,
        }

class Jabatan(db.Model):
    __tablename__ = "tbl_jabatan"

    kdJabatan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    namaJabatan = db.Column(db.String(100), nullable=False)

    def __init__(self, namaJabatan):
        self.namaJabatan = namaJabatan

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, namaJabatan):
        self.namaJabatan = namaJabatan
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all():
        return Jabatan.query.all()

    def get_by_id(id):
        return Jabatan.query.filter_by(kdJabatan=id).first()

    def json(self):
        return {
            'kdJabatan': self.kdJabatan,
            'namaJabatan': self.namaJabatan,
        }

class Departemen(db.Model):
    __tablename__ = "tbl_departemen"

    kdDepartemen = db.Column(db.Integer, primary_key=True, autoincrement=True)
    namaDepartemen = db.Column(db.String(100), nullable=False)
    users = db.relationship('User', backref='user', lazy='dynamic')

    def __init__(self, namaDepartemen):
        self.namaDepartemen = namaDepartemen

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, namaDepartemen):
        self.namaDepartemen = namaDepartemen
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all():
        return Departemen.query.all()

    def get_by_id(id):
        return Departemen.query.filter_by(kdDepartemen=id).first()

    def json(self):
        return {
            'kdDepartemen': self.kdDepartemen,
            'namaDepartemen': self.namaDepartemen,
        }

class UnitKerja(db.Model):
    __tablename__ = "tbl_unitkerja"

    kdUnitKerja = db.Column(db.Integer, primary_key=True, autoincrement=True)
    namaUnitKerja = db.Column(db.String(100), nullable=False)

    def __init__(self, namaUnitKerja):
        self.namaUnitKerja = namaUnitKerja

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, namaUnitKerja):
        self.namaUnitKerja = namaUnitKerja
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all():
        return UnitKerja.query.all()

    def get_by_id(id):
        return UnitKerja.query.filter_by(kdUnitKerja=id).first()

    def json(self):
        return {
            'kdUnitKerja': self.kdUnitKerja,
            'namaUnitKerja': self.namaUnitKerja,
        }

class User(db.Model):
    __tablename__ = "tbl_users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nikUser = db.Column(db.String(255))
    namaLengkap = db.Column(db.String(255))
    tempatLahir = db.Column(db.String(50))
    tanggalLahir = db.Column(db.Integer)
    photo = db.Column(db.String(255))
    kdJenisKelamin = db.Column(db.Integer, db.ForeignKey('tbl_jeniskelamin.kdJenisKelamin'))
    namaJenisKelamin = db.Column(db.String(15))
    kdPendidikan = db.Column(db.Integer, db.ForeignKey('tbl_pendidikan.kdPendidikan'))
    namaPendidikan = db.Column(db.String(100))
    kdDepartemen = db.Column(db.Integer, db.ForeignKey('tbl_departemen.kdDepartemen'))
    namaDepartemen = db.Column(db.String(100))
    kdUnitKerja = db.Column(db.Integer, db.ForeignKey('tbl_unitkerja.kdUnitKerja'))
    namaUnitKerja = db.Column(db.String(100))
    kdJabatan = db.Column(db.Integer, db.ForeignKey('tbl_jabatan.kdJabatan'))
    namaJabatan = db.Column(db.String(100))
    namaPerusahaan = db.Column(db.String(100))
    profile = db.Column(db.String(50))

    def __init__(
            self, 
            email, 
            password, 
            profile, 
            nama, 
            perusahaan, 
            nik_user=None,
            tempat_lahir=None, 
            tanggal_lahir=None,
            kd_jk=None,
            nama_jk=None,
            kd_pendidikan=None,
            nama_pendidikan=None,
            kd_jabatan=None,
            nama_jabatan=None,
            kd_departemen=None,
            nama_departemen=None,
            kd_unit_kerja=None,
            nama_unit_kerja=None
        ):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.profile = profile
        self.namaLengkap = nama
        self.namaPerusahaan= perusahaan
        self.nikUser = nik_user
        self.tempatLahir = tempat_lahir
        self.tanggalLahir= tanggal_lahir
        self.kdJenisKelamin= kd_jk
        self.namaJenisKelamin= nama_jk
        self.kdPendidikan= kd_pendidikan
        self.namaPendidikan= nama_pendidikan
        self.kdJabatan= kd_jabatan
        self.namaJabatan= nama_jabatan
        self.kdDepartemen= kd_departemen
        self.namaDepartemen= nama_departemen
        self.kdUnitKerja= kd_unit_kerja
        self.namaUnitKerja= nama_unit_kerja

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.encode_auth_token(self.id)

    def save_pegawai(self):
        db.session.add(self)
        db.session.commit()

    def update_pegawai(self):
        db.session.add(self)
        db.session.commit()

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.now() + datetime.timedelta(
                    days=app.config.get('AUTH_TOKEN_EXPIRY_DAYS'),
                    seconds=app.config.get('AUTH_TOKEN_EXPIRY_SECONDS')
                ),
                'iat': datetime.datetime.now(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(token):
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({
                'status': 'failed',
                'message': 'Signature expired, Please sign in again'
            })), 401
        except jwt.InvalidTokenError:
            return make_response(jsonify({
                'status': 'failed',
                'message': 'Invalid token. Please sign in again'
            })), 401

    @staticmethod
    def get_by_id(user_id):
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    def is_admin_or_hr(user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            if user.profile == 'admin_perusahaan':
                return True
            elif user.namaDepartemen == 'HRD':
                return True
            return False
        return False
            
    def reset_password(self, new_password):
        self.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()

    def generate_email(email, nama_perusahaan):
        g_email = f'{email}@{nama_perusahaan}.com'
        return g_email

    def generate_password(length):
        password = ''.join((random.choice(string.ascii_lowercase) for x in range(length)))
        return password

    def get_pegawai_hrd(perusahaan):
        return User.query.filter_by(kdDepartemen = 1, namaPerusahaan=perusahaan).all()

    def get_all_pegawai(perusahaan):
        return User.query.filter_by(namaPerusahaan=perusahaan).all()

class AbsensiStatus(db.Model):
    __tablename__ = 'tbl_absensi_status'

    kdStatus = db.Column(db.Integer, primary_key=True, autoincrement=True)
    namaStatus = db.Column(db.String(10), nullable=False)

    def __init__(self, nama_status):
        self.namaStatus = nama_status

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_all():
        return AbsensiStatus.query.all()

    def get_in_status():
        return AbsensiStatus.query.filter_by(namaStatus='Masuk').first()

    def get_by_status(status_id):
        return AbsensiStatus.query.filter_by(kdStatus=status_id).first()

    def json(self):
        return {
            'kdStatus': self.kdStatus,
            'namaStatus': self.namaStatus,
        }

class Absensi(db.Model):
    __tablename__ = 'tbl_absensi'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUser = db.Column(db.Integer, db.ForeignKey('tbl_users.id'))
    namaLengkap = db.Column(db.String(255), nullable=False)
    tglAbsensi = db.Column(db.Integer, nullable=False)
    jamMasuk = db.Column(db.Integer)
    jamKeluar = db.Column(db.Integer)
    kdStatus = db.Column(db.Integer, db.ForeignKey('tbl_absensi_status.kdStatus'))
    namaStatus = db.Column(db.String(10), nullable=False)

    def __init__(self, 
            user_id, 
            nama, 
            tgl_absen, 
            jam_masuk, 
            jam_keluar, 
            kd_status, 
            status
        ):
        self.idUser = user_id
        self.namaLengkap = nama
        self.tglAbsensi = tgl_absen
        self.jamMasuk = jam_masuk
        self.jamKeluar = jam_keluar
        self.kdStatus = kd_status
        self.namaStatus = status

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.add(self)
        db.session.commit()

    def absensi_pegawai(user_id, tgl_awal, tgl_akhir):
        return Absensi.query.filter(Absensi.idUser == user_id) \
            .filter(Absensi.tglAbsensi <= tgl_akhir) \
            .filter(Absensi.tglAbsensi >= tgl_awal) \
            .all()
        
    def list_absensi_pegawai(tgl_awal, tgl_akhir):
        return Absensi.query.filter(Absensi.tglAbsensi <= tgl_akhir) \
            .filter(Absensi.tglAbsensi >= tgl_awal).all()
