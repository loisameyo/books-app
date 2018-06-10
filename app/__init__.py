from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

POSTGRES = {
    'user':'postgres',
    'passwd':'L0C!',
    'db':'postgres',
    'host':'localhost',
    'port':'5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(passwd)s@%(host)s:%(port)s/%(db)s' % POSTGRES

app.url_map.strict_slashes = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret'
db = SQLAlchemy(app)
