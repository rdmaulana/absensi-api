from app import bcrypt
from flask import Blueprint, request
from flask.views import MethodView
from app.models import User
from app.auth.helper import (
    response, 
    response_auth_register, 
    response_auth_login, 
    token_required
)

auth = Blueprint('auth', __name__)

class RegisterUser(MethodView):
    def post(self):
        if request.content_type == 'application/json':
            post_data = request.get_json()
            nama_admin : str = post_data.get('namaAdmin')
            perusahaan : str = post_data.get('perusahaan')

            if nama_admin and perusahaan:
                email = User.generate_email(nama_admin.replace(" ", "_").lower(), "demo")
                password = User.generate_password(8)
                profile = 'admin_perusahaan'
                user = User.get_by_email(email)
                if not user:
                    user_dt = User(
                        email=email, 
                        password=password, 
                        profile=profile, 
                        nama=nama_admin,
                        perusahaan=perusahaan
                    )
                    user_dt.save()
                    return response_auth_register(email, password, profile, 201)
                else:
                    return response('failed', 'Failed, User already exists, Please sign In', 400)
            return response('failed', 'Missing attribute namaAdmin or perusahaan', 400)
        return response('failed', 'Content-type must be json', 400)

class LoginUser(MethodView):
    def post(self):
        if request.content_type == 'application/json':
            post_data = request.get_json()
            email = post_data.get('email')
            password = post_data.get('password')
            profile = post_data.get('profile')

            if email and password and profile:
                user = User.query.filter_by(email=email).first()
                if user and bcrypt.check_password_hash(user.password, password):
                    return response_auth_login(user.encode_auth_token(user.id), user, 200)
                return response('gagal', 'User tidak ditemukan atau password salah', 401)
            return response('gagal', 'Atribut form tidak lengkap', 401)
        return response('gagal', 'Content-type must be json', 202)

class LogoutUser(MethodView):
    def post(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                return response('gagal', 'Masukkan token auth yang valid', 403)
            else:
                decoded_token_response = User.decode_auth_token(auth_token)
                if not isinstance(decoded_token_response, str):
                    return response('success', 'Successfully logged out', 200)
                return response('failed', decoded_token_response, 401)
        return response('failed', 'Provide an authorization header', 403)

@auth.route('/ubah-password-sendiri', methods=['POST'])
@token_required
def reset_password(current_user):
    if request.content_type == "application/json":
        data = request.get_json()
        old_password = data.get('passwordAsli')
        new_password = data.get('passwordBaru1')
        password_confirmation = data.get('passwordBaru2')
        if not old_password or not new_password or not password_confirmation:
            return response('gagal', "Atribut form tidak lengkap", 400)
        if bcrypt.check_password_hash(current_user.password, old_password.encode('utf-8')):
            if not new_password == password_confirmation:
                return response('gagal', 'password tidak sama', 400)
            if not len(new_password) > 6:
                return response('gagal', 'Password baru minimal memilik lebih dari 6 karakter', 400)
            current_user.reset_password(new_password)
            return response('sukses', 'Password reset berhasil', 200)
        return response('gagal', "Password salah", 401)
    return response('gagal', 'Content type must be json', 400)

registration_view = RegisterUser.as_view('register')
login_view = LoginUser.as_view('login')
logout_view = LogoutUser.as_view('logout')

auth.add_url_rule('/init-data', view_func=registration_view, methods=['POST'])
auth.add_url_rule('/login', view_func=login_view, methods=['POST'])
auth.add_url_rule('/logout', view_func=logout_view, methods=['POST'])