from flask import Flask

from app import app


if __name__=='__main__':
    app.config ['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://postgres:L0C!@localhost:5432/books-api'
    #usually the DB_USER://PASSWORD@HOST:PORT/THE DATABASE
    app.run()
