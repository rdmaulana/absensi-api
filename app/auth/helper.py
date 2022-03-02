from flask import request, make_response, jsonify
from functools import wraps
from app.models import User
import jwt
from app import app

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return make_response(jsonify({
                    'status': 'failed',
                    'message': 'Provide a valid auth token'
                })), 403

        if not token:
            return make_response(jsonify({
                'status': 'failed',
                'message': 'Token is missing'
            })), 401

        try:
            decode_response = User.decode_auth_token(token)
            current_user = User.query.filter_by(id=decode_response).first()
        except:
            message = 'Invalid token'
            if isinstance(decode_response, str):
                message = decode_response
            return make_response(jsonify({
                'status': 'failed',
                'message': message
            })), 401

        return f(current_user, *args, **kwargs)

    return decorated_function

def response(status, message, status_code):
    return make_response(jsonify({
        'status': status,
        'message': message
    })), status_code

def response_auth_register(email : str, password : str, profile : str, status_code : int):
    return make_response(jsonify({
        'email': email,
        'password': password,
        'profile': profile,
    })), status_code

def response_auth_login(token, user_info, status_code : int):
    return make_response(jsonify({
        'hasil': {
            'token': token,
            'info': {
                'profile': user_info.profile,
                'idUser': user_info.id,
                'namaLengkap': user_info.namaLengkap,
                'tempatLahir': user_info.tempatLahir,
                'tanggalLahir': user_info.tanggalLahir,
                'email': user_info.email,
                'password': user_info.password,
                'nikUser': user_info.nikUser,
                'kdJabatan': user_info.kdJabatan,
                'namaJabatan': user_info.namaJabatan,
                'kdDepartemen': user_info.kdDepartemen,
                'namaDepartemen': user_info.namaDepartemen,
                'kdUnitKerja': user_info.kdUnitKerja,
                'namaUnitKerja': user_info.namaUnitKerja,
                'kdJenisKelamin': user_info.kdJenisKelamin,
                'namaJenisKelamin': user_info.namaJenisKelamin,
                'kdPendidikan': user_info.kdPendidikan,
                'namaPendidikan': user_info.namaPendidikan,
                'photo': user_info.photo
            }
        }
    })), status_code