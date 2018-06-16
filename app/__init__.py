from flask import Flask
from flask import Response, request, json, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import migrate
from flask_jwt_extended import JWTManager
from config import Config

app = Flask(__name__)


jwt = JWTManager(app)
app.secret_key = 'secret'

app.url_map.strict_slashes = False

POSTGRES = {
    'user':'postgres',
    'passwd':'L0C!',
    'db':'books_api',
    'host':'localhost',
    'port':'5432',
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(passwd)s@%(host)s:%(port)s/%(db)s' % POSTGRES

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'jwt-token-secret-key'


# Initialize Flask Sql Alchemy
db = SQLAlchemy(app)

