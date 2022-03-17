import os

class Config:   
 SECRET_KEY = os.environ.get('SECRET_KEY')
 SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:sieva@localhost/climate'
 SQLALCHEMY_TRACK_MODIFICATIONS= False

class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}