from flask import Flask
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import timedelta

from app import db



"""Defining tables models"""


class MainModel(db.Model):
    # This is a base data model for all objects. Other models will inherit properties from here
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        # Define a standard way to print models
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self.__to__dict().items()
        })

    def json(self):
        # Define a standard way to jsonify models, dealing with datetime objects

        return{
            column: value if not isinstance(
                value, datetime.date) else value.strftime('%Y-%M-%D')
            for column, value in self.__to__dict().items()
        }


class UsersTable(MainModel, db.Model):
    """This is a model for the users table"""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True, nullable=False)
    usermail = db.Column(db.String(30), unique=True, nullable=False)
    passwd_hash = db. Column(db.String(30))
    is_admin = db.Column(db.Boolean, default=False)

    def register(self):
        db.session.add(self)
        db.session.commit()

    def retrieve_all(self):
        return UsersTable.query.all()

    def retrieve_user_by_usermail(self, usermail):
        return UsersTable.query.filter_by(usermail=usermail).first()  # why not ==

    def hash_user_passwd(self, passwd):
        """hash a password given by a suser"""
        self.passwd_hash = generate_password_hash(passwd)

    def verify_passwd(self, passwd):
        """Check if the password given by a user is valid"""
        return check_password_hash(self.passwd_hash, passwd)



class Library(db.Model):
    """This is a model for the books table"""
    __tablename__ = 'books'
 
    book_id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(30), unique=True, nullable=False)
    book_author = db.Column(db.String(30), unique=True, nullable=False)
    publication_year = db.Column(db.Integer)
    is_not_borrowed = db.Column(db.Boolean, default=True)
  

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

    @property
    def serialize(self):
        return {
            "Book ID": self.book_id,
            "Book Title": self.book_title,
            "Book Author": self.book_author,
            "Publication year": self.publication_year,
            "Status": self.is_not_borrowed
        }


class UserHistory(MainModel, db.Model):
    """This model displays the borrowing history of a user"""
    __tablename__ = 'user_history'
    logon_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)
    book_title = db.Column(db.String(30))
    username = db.Column(db.String(60))
    usermail = db.Column(db.String(60))
    date_borrowed = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)
    book_returned = db.Column(db.Boolean, default=False)

    def save_book(self):
        db.session.add(self)
        db.session.commit()

    def get_user_history(self, usermail):
        return UserHistory.query.filter_by(usermail=usermail).all()

    def get_unreturned_books(self, usermail):
        return UserHistory.query.filter_by(usermail=usermail, book_returned=False).all()

    def retrieve_book_by_id(self, book_id):
        return UserHistory.query.filter_by(book_id=book_id, book_returned=False).first()

    @property
    def serialize(self):
        """ Serialize the class UserHistory when this function is called."""
        return{

            "Username": self.username,
            "Book ID": self.book_id,
            "Book Title": self.book_title,
            "Date Borrowed": self.date_borrowed,
            "Due Date": self.return_date,
            "Book Returned": self.book_returned
        }


class IssuedTokens(MainModel, db.Model):
    """This class represents tokens issued table"""
    __tablename__ = 'issued_tokens'
    token_id = db.Column(db.Integer, primary_key=True)
    revoke_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    jti = db.Column(db.String(200), unique=True)

    def token_revoke(self):
        db.session.add(self)
        db.session.commit()

    def is_jti_blacklisted(self, jti):  # method should have self as first argument
        query = IssuedTokens.query.filter_by(jti=jti).first()
        if query:
            return True
        return False


class ActiveTokens(MainModel, db.Model):
    """"""
    __tablename__ = 'active_tokens'
    token_id = db.Column(db.Integer, primary_key=True)
    token_time_created = db.Column(
        db.DateTime, default=db.func.current_timestamp())
    user_usermail = db.Column(db.String, unique=True)
    access_token = db.Column(db.String, unique=True)

    def __init__(self, user_usermail, access_token):
        self.user_usermail = user_usermail
        self.access_token = access_token

    def save_issued_token(self):
        db.session.add(self)
        db.seesion.commit()

    def delete_active_token(self):
        db.session.delete(self)
        db.session.commit

    def token_is_expired(self):
        return (datetime.now() - self.time_created) > timedelta(minutes=15)

    def find_user_with_issed_token(self, user_usermail):
        return ActiveTokens.query.filter_by(user_usermail=user_usermail).first()
