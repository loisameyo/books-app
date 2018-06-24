from flask import json, jsonify
import unittest
import os, json
from app import create_app, db
from app.models import BooksTable
from config import app_config


class UserTests(unittest.TestCase):
    def setUp(self):
        # """Initialize and define variables for testing."""
        config_name = 'testing'
        self.app = create_app(config_name)
        self.test_client = self.app.test_client()
        self.app.app_context()
        self.app.app_context().push()
        with self.app.app_context():
            db.create_all()

        
        self.user= {'name': 'Odi', 'email': 'loice@gmail.com', 'password': 'Loice1' }
        self.book= {'title':'Ruby goes to Mars','author':'Odi Meyo', 'year':'2002','is_not_borrowed':True}
        self.book2= {'title':'Ruby and Rono go to Mars','author':'Odi Meyo', 'year':'2002','is_not_borrowed':True}
        self.login = {'email': 'loiceadmin@gmail.com', 'password': 'Loiceadm1',}
        self.book_1  = BooksTable(book_title=self.book['title'], book_author=self.book['author'], publication_year=self.book['year'])
        self.book_2  = BooksTable(book_title=self.book2['title'], book_author=self.book2['author'], publication_year=self.book2['year'])

    def register_and_login_user(self):
        # Register a new user
        self.test_client.post('/api/v2/auth/register', data=json.dumps(self.user), 
            headers={'content-type':'application/json'})

        # Login a user
        login_response = self.test_client.post(
            '/api/v2/auth/login', data=json.dumps(self.user), headers={'content-type':'application/json'})
        self.assertEqual(login_response.status_code, 200)
        # Get user access token
        access_token = json.loads(login_response.data)['access_token']
        return access_token
    
    def test_borrow_book_without_valid_token(self):
        self.book_1.save_book_to_db()
        response = self.test_client.post('/api/v2/users/books/1', 
        data=json.dumps({'email':self.user['email']}), headers = {'content-type':'application/json'})
        self.assertEqual(response.status_code, 401)
    
    def test_borrow_book(self):
        access_token=self.register_and_login_user()
        headers = {'content-type':'application/json', 'authorization': 'Bearer {}'.format(access_token)}
        self.book_1.save_book_to_db()

        response = self.test_client.post('/api/v2/users/books/1', 
        data=json.dumps({'email':self.user['email']}),headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('You have successfully borrowed a book', json.loads(response.data)['Message'])

    def test_borrow_nonexistent_book(self):
        access_token=self.register_and_login_user()
        headers = {'content-type':'application/json', 'authorization': 'Bearer {}'.format(access_token)}
        self.book_1.save_book_to_db()

        response = self.test_client.post('/api/v2/users/books/2', 
        data=json.dumps({'email':self.user['email']}),headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual('The library has no book with that ID', json.loads(response.data)['message'])

         
    def test_return_book(self):
        access_token=self.register_and_login_user()
        headers = {'content-type':'application/json', 'authorization': 'Bearer {}'.format(access_token)}
        self.book_1.save_book_to_db()
        self.test_client.post('/api/v2/users/books/1', 
        data=json.dumps({'email':self.user['email']}),headers=headers)
        response = self.test_client.put('/api/v2/users/books/1', data=json.dumps({'email':self.user['email']}),headers=headers)
        self.assertEqual(response.status_code, 200)
    
    def test_return_book_not_borrowed(self):
        access_token=self.register_and_login_user()
        headers = {'content-type':'application/json', 'authorization': 'Bearer {}'.format(access_token)}
        self.book_1.save_book_to_db()
        self.book_2.save_book_to_db()
        self.test_client.post('/api/v2/users/books/1', 
        data=json.dumps({'email':self.user['email']}),headers=headers)
        response = self.test_client.put('/api/v2/users/books/2', data=json.dumps({'email':self.user['email']}),headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual('This book has not been borrowed {}'.format(self.book_2.book_title), json.loads(response.data)['Message'])

    def tearDown(self):
        """Return to normal state after test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()