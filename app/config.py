import os
from os.path import join, dirname
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
dotenv_path = join(dirname(__file__), './../.env')
load_dotenv(dotenv_path)

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    BCRYPT_HASH_PREFIX = 14
    BCRYPT_LOG_ROUNDS = 12
    AUTH_TOKEN_EXPIRY_DAYS = 30
    AUTH_TOKEN_EXPIRY_SECONDS = 3000

    UPLOAD_FOLDER = os.environ['UPLOAD_FOLDER']
    MAX_FILE_LENGTH = 2 * 1024 * 1024 #2MB

def allowed_file_upload(filename):
    EXTENSTION_FILE_UPLOAD = set(['jpg', 'png', 'jpeg'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSTION_FILE_UPLOAD

class DevelopmentConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, './../db_test.sqlite3')
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL_TEST']
    BCRYPT_HASH_PREFIX = 4
    AUTH_TOKEN_EXPIRY_DAYS = 0
    AUTH_TOKEN_EXPIRY_SECONDS = 3
    AUTH_TOKEN_EXPIRATION_TIME_DURING_TESTS = 5

class ProductionConfig(BaseConfig):
    DEBUG = False
