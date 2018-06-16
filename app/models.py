from flask import Flask
from werkzeug.security import check_password_hash, generate_password_hash
# from flask_sqlalchemy import SQLAlchemy 
# from flask_migrate import migrate
# from sqlalchemy.orm import backref
from datetime import datetime, timedelta


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

    def save(self):

        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_record(cls, **kwargs):
        cls.query.filter_by(**kwargs).first()

class UsersTable(MainModel, db.Model):
    """This is a model for the users table"""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12),unique=False, nullable=False)
    usermail = db.Column(db.String(30), unique=True, nullable=False)
    passwd_hash = db.Column(db.String(500))
    is_admin = db.Column(db.Boolean, default=False)
    logged_in = db.Column(db.Boolean, default = False)
    
    user_book_history = db.relationship('BookHistory', backref = 'UsersTable', lazy = True)

    def __init__(self, username, usermail, passwd_hash):
        self.username = username
        self.usermail = usermail
        self.passwd_hash =passwd_hash

    def register(self):
        db.session.add(self)
        db.session.commit()

    def retrieve_all(self):
        return UsersTable.query.all()

    @staticmethod
    def retrieve_user_by_email(usermail):
        return UsersTable.query.filter_by(usermail=usermail).first()

    def hash_user_passwd(self, passwd):
        """hash a password given by a user"""
        self.passwd_hash = generate_password_hash(passwd)

    def verify_passwd(self, passwd):
        """Check if the password given by a user is valid"""
        return check_password_hash(self.passwd_hash, passwd)
    @staticmethod
    def verify_username (username):
        if UsersTable.query.filter_by(username=username).count() > 0:
            return False
        return True


class Library(db.Model):
    """This is a model for the books table"""
    __tablename__ = 'books'
 
    book_id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(30), unique=True, nullable=False)
    book_author = db.Column(db.String(30), unique=True, nullable=False)
    publication_year = db.Column(db.Integer)
    is_not_borrowed = db.Column(db.Boolean, default=True)
    
    book_history = db.relationship('BookHistory', backref = 'Library', lazy = True)
  

    def save_book_to_db(self):
        db.session.add()
        db.session.commit()

    def retrieve_all_books(self):
        return Library.query.all()

    def retrieve_book_by_id(self, book_id):
        return Library.query.filter_by(book_id=book_id).first()

    def delete_book(self):
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


class BookHistory(db.Model):
    """This model displays the borrowing history of a user"""
    __tablename__ = 'book_history'

    session_id = db.Column(db.Integer, primary_key = True)
    
    username = db.Column(db.String(60))
    book_title = db.Column(db.String(30))
    time_borrowed = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_borrowed = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)
    book_returned = db.Column(db.Boolean, default=False)
    user_history = db.Column(db.String, db.ForeignKey(UsersTable.usermail))
    book_history = db.Column(db.Integer, db.ForeignKey(Library.book_id))

    def save_book_to_db(self):
        db.session.add(self)
        db.session.commit()

    def get_user_history(self, usermail):
        return BookHistory.query.filter_by(usermail=usermail).all()

    def get_unreturned_books(self, usermail):
        return BookHistory.query.filter_by(usermail=usermail, book_returned=False).all()

    def retrieve_book_by_id(self, book_id):
        return BookHistory.query.filter_by(book_id=book_id, book_returned=False).first()

    @property
    def serialize(self):
        """ Serialize the class BookHistory when this function is called."""
        return{

            "Username": self.username,
            "User Email": self.usermail,
            "Book ID": self.book_id,
            "Book Title": self.book_title,
            "Date Borrowed": self.date_borrowed,
            "Due Date": self.return_date,
            "Book Returned": self.book_returned
        }


class IssuedTokens(db.Model):
    """This class represents tokens issued table"""
    __tablename__ = 'issued_tokens'
    token_id = db.Column(db.Integer, primary_key=True)
    revoke_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    jti = db.Column(db.String(500), unique=True)
    def __init__(self, jti):
        self.jti = jti

    def save(self):
        db.session.add(self)
        db.session.commit()

    def token_revoke(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def is_jti_blacklisted(jti):
        query = IssuedTokens.query.filter_by(jti=jti).first()
        if query:
            return True
        return False


class ActiveTokens(db.Model):
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
        db.session.commit()

    def delete_active_token(self):
        db.session.delete(self)
        db.session.commit()

    def token_is_expired(self):
        return (datetime.now() - self.time_created) > timedelta(minutes=15)

    @staticmethod
    def find_user_with_issued_token(user_usermail):
        if ActiveTokens.query.filter_by(user_usermail=user_usermail).count() > 0:
            return False
        return True

    @staticmethod
    def get_access_token(user_usermail):
        return ActiveTokens.query.filter_by(user_usermail=user_usermail).first()
