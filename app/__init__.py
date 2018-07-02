from flask import Flask
from flask import Response, request, json, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import migrate
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from config import app_config
from .error_handlers import route_not_found, method_not_found
from .error_handlers import internal_server_error
                       

db = SQLAlchemy()
mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'secret'
    db.init_app(app)
    app.url_map.strict_slashes = False
    app.config['JWT_SECRET_KEY'] = 'jwt-token-secret-key'
    jwt = JWTManager(app)

    # Register blueprints
    from app.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix="/api/v2")

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/api/v2/auth")

    from app.books import book as book_blueprint
    app.register_blueprint(book_blueprint, url_prefix="/api/v2/books")

    from app.user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix="/api/v2/users")

    app.register_error_handler(404, route_not_found)
    app.register_error_handler(405, method_not_found)
    app.register_error_handler(500, internal_server_error)
    
    

    return app
