from flask import Flask
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import backref
from datetime import datetime, timedelta


from app import db

"""Defining tables models"""

class UsersTable(db.Model):
    """This is a model for the users table"""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12),unique=False, nullable=False)
    usermail = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(500))
    is_admin = db.Column(db.Boolean, default=False)
    logged_in = db.Column(db.Boolean, default = False)
    user_history = db.relationship('BookHistory', backref = 'user')

    def __init__(self, username, usermail, password_hash):
        self.username = username
        self.usermail = usermail
        self.password_hash =password_hash

    def register(self):
        db.session.add(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def retrieve_all(self):
        return UsersTable.query.all()

   
    def retrieve_user_by_email(usermail):
        return UsersTable.query.filter_by(usermail=usermail).first()

    def hash_user_password(self, password):
        """hash a password given by a user"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Check if the password given by a user is valid"""
        return check_password_hash(self.password_hash, password)
    @staticmethod
    def verify_username (username):
        if UsersTable.query.filter_by(username=username).count() > 0:
            return False
        return True
    
    @property
    def serialize(self):
        return {
            "User ID": self.user_id,
            "Name": self.username,
            "Status": self.is_admin
            
        }
   

class BooksTable(db.Model):
    """This is a model for the books table"""
    __tablename__ = 'books'
 
    book_id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(30), unique=True, nullable=False)
    book_author = db.Column(db.String(30), nullable=False)
    publication_year = db.Column(db.Integer)
    is_not_borrowed = db.Column(db.Boolean, default=True)
    book_history = db.relationship('BookHistory', backref = 'book')
  

    def save_book_to_db(self):
        db.session.add(self)
        db.session.commit()

    def retrieve_all_books(self):
        return BooksTable.query.all()

    def retrieve_book_by_id(self, book_id):
        return BooksTable.query.filter_by(book_id=book_id).first()
    
    def retrieve_book_by_title_author_year(title, author, year):
        return BooksTable.query.filter_by(book_title=title, book_author=author, publication_year=year).first()

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

    @property
    def serialize_history(self):
        return {
            "Book Title": self.book_title,
            "Book Author": self.book_author
        }

class BookHistory(db.Model):
    """This model displays the borrowing history of a user"""
    __tablename__ = 'book_history'

    session_id = db.Column(db.Integer, primary_key = True)
    date_borrowed = db.Column(db.DateTime, default=db.func.current_timestamp())
    return_date = db.Column(db.DateTime)
    book_returned = db.Column(db.Boolean, default=False)
    bh_usermail = db.Column(db.String, db.ForeignKey(UsersTable.usermail))
    bh_book_id = db.Column(db.Integer, db.ForeignKey(BooksTable.book_id))

    def save_book_to_db(self):
        db.session.add(self)
        db.session.commit()

    def get_user_history(usermail):
        return BookHistory.query.filter_by(bh_usermail=usermail).all()

    def get_unreturned_books(usermail):
        return BookHistory.query.filter_by(bh_usermail=usermail, book_returned=False).all()

    def retrieve_book_by_id_and_usermail(book_id, usermail):
        return BookHistory.query.filter_by(bh_book_id=book_id, bh_usermail=usermail).first()

    @property
    def serialize(self):
        """ Serialize the class BookHistory when this function is called."""
        return{

           
            "User Email": self.bh_usermail,
            "Book ID": self.bh_book_id,
            "Date Borrowed": self.date_borrowed,
            "Due Date": self.return_date,
            "Book Returned": self.book_returned
        }


class RevokedTokens(db.Model):
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
        query = RevokedTokens.query.filter_by(jti=jti).first()
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
        return (datetime.now() - self.token_time_created) > timedelta(minutes=30)

    @staticmethod
    def find_user_with_issued_token(user_usermail):
        return ActiveTokens.query.filter_by(user_usermail=user_usermail).first()
