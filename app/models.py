from flask import Flask
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
import datetime

from app import db


"""Defining tables models"""
class MainModel(db.Model):
    #This is a base data model for all objects. Other models will inherit properties from here
    __abstract__ = True
    def __init__(self, *args):
        super().__init__(*args)
    def __repr__(self):
        #Define a standard way to print models
        return '%s(%s)' % (self.__class__.__name__,{
            column:value
            for column, value in self.__to__dict().items()
        })
    def json(self):
    #Define a standard way to jsonify models, dealing with datetime objects
    
        return{
        column: value if not isinstance(value, datetime.date) else  value.strftime('%Y-%M-%D')
        for column, value in self.__to__dict().items()
        }
    


class UsersTable(MainModel, db.Model):
    """This is a model for the users table"""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique = True, nullable = False)
    email = db.Column(db.String(30), unique = True, nullable = False)
    passwd_hash = db. Column(db.String(30))
    is_admin = db.Column(db.Boolean, default=False)

    def register(self):
        db.session.add(self)
        db.session.commit()

    def retrieve_all(self):
        return UsersTable.query.all()
    
    def retrieve_user_by_email(self, email):
        return UsersTable.query.filter_by(email = email).first() #why not ==
    
    def hash_user_passwd (self, passwd):
        """hash a password given by a suser"""
        self.passwd_hash = generate_password_hash(passwd)
    
    def verify_passwd(self, passwd):
        """Check if the password given by a user is valid"""
        return check_password_hash(self.passwd_hash, passwd)


class Library(MainModel, db.Model):
     """This is a model for the books table"""
     __tablename__ = 'books'
     book_id = db.Column(db.Integer, primary_key=True)
     book_title = db.Column(db.String(30), unique = True, nullable = False)
     book_author = db.Column(db.String(30), unique = True, nullable = False)
     publication_year = db.Column(db.Integer)
     is_borrowed = db.Column(db.Boolean, default=False)

     def save_book(self):
         db.session.add(self)
         db.session.commit()
     
     def retrieve_all_books(self):
         return Library.query.all()        
    
     def retrieve_book_by_id(self, book_id):
         return Library.query.filter_by(book_id=book_id).first()
    
     def delete_book(self, bookd_id):
         db.session.delete(self)
         db.session.commit()

class UserHistory(MainModel, db.Model):
    """This model displays the borrowing history of a user"""
    __tablename__ = 'user_history'

