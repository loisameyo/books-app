from flask import Flask

from app import app
from app import views
from app.auth import auth


if __name__=='__main__':
    app.config ['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql:///books_api'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # # usually the DB_USER://PASSWORD@HOST:PORT/THE DATABASE
    app.run(debug=True)
