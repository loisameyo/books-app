
import os

class Config(object):
    """Configuration setting for the db."""   
    DEBUG = False
    ADMIN = "meyoodi18@gmail.com"
    SECRET = os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
    # mail configuration
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USER')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('MAIL_USER')
    MAIL_PASSWORD = os.getenv('MAIL_PASS')

class DevelopmentConfig(Config):
    """Configuration setting at development stage."""
    SQLALCHEMY_DATABASE_URI= os.getenv('DATABASE_URL')
    DEBUG = True


class TestingConfig(Config):
    """Configuration setting at testing stage"""
    SQLALCHEMY_DATABASE_URI= os.getenv('TEST_DATABASE_URL')
    DEBUG = True

class ProductionConfig(Config):
    """Configuration setting at production stage"""
    SQLALCHEMY_DATABASE_URI= os.getenv('DATABASE_URL')
    DEBUG = False





app_config = {
    'development': DevelopmentConfig,
    'production':ProductionConfig,
    'testing':TestingConfig
    
}