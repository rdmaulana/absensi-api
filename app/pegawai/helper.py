from flask import make_response, jsonify

def response(status, message, code):
    return make_response(jsonify({
        'status': status,
        'message': message
    })), code

def response_get_json_list(arr):
    return make_response(jsonify(
        arr
    )), 200

def response_created_jkelamin(obj, status_code : int):
    return make_response(jsonify({
        'status': 'success',
        'kdJenisKelamin': obj.kdJenisKelamin,
        'namaJenisKelamin': obj.namaJenisKelamin,
    })), status_code

def response_created_departemen(obj, status_code : int):
    return make_response(jsonify({
        'status': 'success',
        'kdDepartemen': obj.kdDepartemen,
        'namaDepartemen': obj.namaDepartemen,
    })), status_code

def response_created_unit_kerja(obj, status_code : int):
    return make_response(jsonify({
        'status': 'success',
        'kdUnitKerja': obj.kdUnitKerja,
        'namaUnitKerja': obj.namaUnitKerja,
    })), status_code

def response_created_pendidikan(obj, status_code : int):
    return make_response(jsonify({
        'status': 'success',
        'kdPendidikan': obj.kdPendidikan,
        'namaPendidikan': obj.namaPendidikan,
    })), status_code

def response_created_jabatan(obj, status_code : int):
    return make_response(jsonify({
        'status': 'success',
        'kdJabatan': obj.kdJabatan,
        'namaJabatan': obj.namaJabatan,
    })), status_code

def response_created_pegawai(message, status_code : int):
    return make_response(jsonify({
        'status': 'sukses',
        'message': message,
    })), status_code

def response_updated_pegawai(message, status_code : int):
    return make_response(jsonify({
        'status': 'sukses',
        'message': message,
    })), status_code
