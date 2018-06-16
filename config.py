
import os

class Config(object):
    """Common configuration Setting."""
    SQLALCHEMY_DATABASE_URI= os.getenv('DATABASE_URL')
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Configuration setting at development stage."""
    DEBUG = True






app_config = {
    'development': DevelopmentConfig
    
}