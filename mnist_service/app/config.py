import os

class BaseConfig(object):
    DEBUG = os.environ['DEBUG']
    SECRET_KEY = os.environ['SECRET_KEY']
    DB_SERVICE = os.environ['DB_SERVICE']
    DB_PORT = os.environ['DB_PORT']
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']

class DevConfig(BaseConfig):
    POSTGRES_DB = os.environ['POSTGRES_DB_DEV']
    POSTGRES_USER = os.environ['POSTGRES_USER_DEV']
    POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD_DEV']
    SQLALCHEMY_DATABASE_URI = os.environ['POSTGRES_URL_DEV']

class ProdConfig(BaseConfig):
    POSTGRES_DB = os.environ['POSTGRES_DB']
    POSTGRES_USER = os.environ['POSTGRES_USER']
    POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
    SQLALCHEMY_DATABASE_URI = os.environ['POSTGRES_URL']

config = {
    'development': DevConfig,
    'production': ProdConfig,
}
