import os  # allow for interaction with the operating system dependent functionality

class Config:
    '''
    General configuration parent class
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://alvin:german@localhost/perfectpitch'
    UPLOADED_PHOTOS_DEST = 'app/static/photos'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    #email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    @staticmethod
    def init_app(app):
        pass



class ProdConfig(Config):
    """
    Describes production configuration child class
    Args:
        Config: The parent configration class with General configuration settings
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://alvin:german@localhost/perfectpitch_test'

class DevConfig(Config):
    """
    Describes development configuration child class
    Args:
         Config: The parent configuration class with General configuration settings
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://alvin:german@localhost/perfectpitch'
    DEBUG = True

# Dictionary that helps us access the different configuration option classes
config_options = {
    'development': DevConfig,
    'production': ProdConfig
}