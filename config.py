
import os

class Config(object):
    """Configuration setting for the db."""
    SQLALCHEMY_DATABASE_URI= os.getenv('DATABASE_URL')
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Configuration setting at development stage."""
    DEBUG = True


class TestingConfig(Config):
    """Configuration setting at testing stage"""
    SQLALCHEMY_DATABASE_URI = "app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql:///test_books_api'"

class ProductionConfig(Config):
    """Configuration setting at production stage"""
    DEBUG = False
    TESTING = False





app_config = {
    'development': DevelopmentConfig,
    'production':ProductionConfig,
    'testing':TestingConfig
    
}