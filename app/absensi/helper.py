from flask import make_response, jsonify

def response(status, message, code):
    return make_response(jsonify({
        'status': status,
        'message': message
    })), code

def response_get_json_list(arr : list):
    return make_response(jsonify(
        arr
    )), 200

def response_checkin_absen(obj, status_code : int):
    return make_response(jsonify({
        'jamMasuk': obj.jamMasuk,
    })), status_code

def response_checkout_absen(obj, status_code : int):
    return make_response(jsonify({
        'jamKeluar': obj.jamKeluar,
    })), status_code
