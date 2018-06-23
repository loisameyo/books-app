
import os

class Config(object):
    """Configuration setting for the db."""   
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Configuration setting at development stage."""
    SQLALCHEMY_DATABASE_URI= os.getenv('DATABASE_URL')
    DEBUG = True


class TestingConfig(Config):
    """Configuration setting at testing stage"""
    SQLALCHEMY_DATABASE_URI= 'sqlite:///:memory:'
    DEBUG = True

class ProductionConfig(Config):
    """Configuration setting at production stage"""
    SQLALCHEMY_DATABASE_URI= os.getenv('DATABASE_URL')
    DEBUG = False
    TESTING = False





app_config = {
    'development': DevelopmentConfig,
    'production':ProductionConfig,
    'testing':TestingConfig
    
}