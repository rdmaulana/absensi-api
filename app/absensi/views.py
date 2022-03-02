from datetime import datetime
from flask import Blueprint, jsonify, request
from app.auth.helper import token_required
from app.models import (
    Absensi,
    AbsensiStatus,
    User,
    BaseModel
)
from app.absensi.helper import (
    response,
    response_checkin_absen,
    response_checkout_absen,
    response_get_json_list
)
from app.absensi.schema import (
    history_absensi_schema,
    history_absensi_all_schema
)

absensi = Blueprint('absensi', __name__)

@absensi.route('/daftar/admin', methods=["GET"])
@token_required
def history_absensi_pegawai_all(current_user):
    if User.is_admin_or_hr(current_user.id):
        tgl_awal = request.args.get('tglAwal')
        tgl_akhir = request.args.get('tglAkhir')

        if tgl_awal and tgl_akhir:
            absensi_data = Absensi.list_absensi_pegawai(tgl_awal, tgl_akhir)
            result = history_absensi_all_schema.dump(absensi_data)
            return response_get_json_list(result)
        return response("gagal", 'Atribut paramater tidak lengkap', 400)
    return response("gagal", 'Akses ditolak', 401)

@absensi.route('/daftar/pegawai', methods=["GET"])
@token_required
def history_absensi_pegawai(current_user):
    tgl_awal = request.args.get('tglAwal')
    tgl_akhir = request.args.get('tglAkhir')

    if tgl_awal and tgl_akhir:
        absensi_data = Absensi.absensi_pegawai(current_user.id, tgl_awal, tgl_akhir)
        result = history_absensi_schema.dump(absensi_data)
        return response_get_json_list(result)
    return response("gagal", 'Atribut form tidak lengkap', 400)

@absensi.route('/combo/status-absen', methods=["GET"])
@token_required
def get_list_status_absen(current_user):
    list = []
    data = AbsensiStatus.get_all()

    for obj in data:
        list.append(obj.json())
    return response_get_json_list(list)

@absensi.route('/in', methods=["GET"])
@token_required
def check_in_absen(current_user):
    get_status = AbsensiStatus.get_in_status()
    try:
        cek_absensi = Absensi.query.filter_by(
            idUser=current_user.id,
            tglAbsensi=BaseModel.generate_epoc_date()
        ).first()
        if not cek_absensi:
            absensi_dt = Absensi(
                user_id=current_user.id,
                nama=current_user.namaLengkap,
                tgl_absen=BaseModel.generate_epoc_date(),
                jam_masuk=BaseModel.generate_datetime_to_epoc(),
                jam_keluar=None,
                kd_status=get_status.kdStatus,
                status=get_status.namaStatus
            )
            absensi_dt.save()
            return response_checkin_absen(absensi_dt, 201)
        return response("gagal", 'Anda sudah melakukan absen hari ini', 400)
    except Exception as e:
        print(e)
        return response('gagal', 'Absen gagal, silahkan coba kembali', 400)

@absensi.route('/out', methods=["GET"])
@token_required
def check_out_absen(current_user):
    try:
        get_absensi = Absensi.query.filter_by(
            idUser=current_user.id,
            tglAbsensi=BaseModel.generate_epoc_date()
        ).first()
        if get_absensi:
            get_absensi.jamKeluar = BaseModel.generate_datetime_to_epoc()
            Absensi.update(get_absensi)
            return response_checkout_absen(get_absensi, 201)
    except Exception as e:
        print(e)
        return response('gagal', 'Absen gagal, silahkan coba kembali', 400)

@absensi.route('/absensi', methods=["POST"])
@token_required
def create_absensi(current_user):
    if request.content_type == 'application/json': 
        data = request.get_json()
        tgl_absensi = data.get('tglAbsensi')
        kode_status = data.get('kdStatus')

        if tgl_absensi and kode_status:
            get_status = AbsensiStatus.get_by_status(kode_status)
            absensi_dt = Absensi(
                user_id=current_user.id, 
                nama=current_user.namaLengkap, 
                tgl_absen=tgl_absensi, 
                kd_status=kode_status, 
                status=get_status.namaStatus,
                jam_masuk=None,
                jam_keluar=None
            )
            absensi_dt.save()
            return response("sukses", "Berhasil menyimpan absensi", 201)
        return response("gagal", 'Atribut form tidak lengkap', 400)
    return response('failed', 'Content-type must be json', 401)

