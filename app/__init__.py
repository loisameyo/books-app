from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from app import views

db = SQLAlchemy()
app = Flask (__name__)

POSTGRES = {
    'user':'postgres',
    'passwd':'L0C!',
    'db':'books-api',
    'host':'localhost',
    'port':'5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(passwd)s@%(host)s:%(port)s/%(db)s' % POSTGRES

app.url_map.strict_slashes = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret'

db.init_app(app)

from app import views
from app.auth.auth import auth

if __name__ == '__main__':
    app.run()
