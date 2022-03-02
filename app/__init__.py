import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

app = Flask(__name__, static_folder=None)

CORS(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

ma = Marshmallow(app)

migrate = Migrate(app, db)

from app import views

from app.auth.views import auth

app.register_blueprint(
    auth,
    url_prefix='/api/auth/'
)

from app.pegawai.views import pegawai

app.register_blueprint(
    pegawai,
    url_prefix='/api/pegawai/'
)

from app.absensi.views import absensi

app.register_blueprint(
    absensi,
    url_prefix='/api/presensi/'
)

