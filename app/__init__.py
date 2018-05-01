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
app.secret_key = 'secret'

db.init_app(app)



