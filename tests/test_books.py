from flask import json, jsonify
import unittest
import os, json
from app import create_app, db
from app.models import BooksTable
from config import app_config


class EndpointTests(unittest.TestCase):
    def setUp(self):
        # """Initialize and define variables for testing."""
        config_name = 'testing'
        self.app = create_app(config_name)
        self.test_client = self.app.test_client()
        self.app.app_context()
        self.app.app_context().push()
        with self.app.app_context():
            db.create_all()

        self.user1= {'name': 'Odi', 'email': 'loiceadmin@gmail.com', 'password': 'Loiceadm1', 'is_admin': True }
        self.user= {'name': 'Odi', 'email': 'loice@gmail.com', 'password': 'Loice1' }
        self.book= {'title':'Ruby goes to Mars','author':'Odi Meyo', 'year':'2002','is_not_borrowed':True}
        self.book2= {'title':'Ruby and Rono go to Mars','author':'Odi Meyo', 'year':'2002','is_not_borrowed':True}
        self.login = {'email': 'loiceadmin@gmail.com', 'password': 'Loiceadm1',}
        self.book_1  = BooksTable(book_title=self.book['title'], book_author=self.book['author'], publication_year=self.book['year'])
        self.book_2  = BooksTable(book_title=self.book2['title'], book_author=self.book2['author'], publication_year=self.book2['year'])
    def register_and_login_admin(self):
        # Register a new admin
        self.test_client.post(
            '/api/v2/auth/register', data=json.dumps(self.user1), headers={'content-type':'application/json'})
        
        # Login an admin
        login_response = self.test_client.post(
            '/api/v2/auth/login', data=json.dumps(self.login),headers={'content-type':'application/json'})
        # Get admin access token
        access_token = json.loads(login_response.get_data().decode('utf-8'))['access_token']

        return access_token

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

    def test_admin_adding_book(self):
        """Test if an admin can add a book without an access token"""
        response = self.test_client.post('/api/v2/books', data=json.dumps({'title': 'Beginning Python', 'author': 'J Wachira',
         'pub_year': '2000'}), headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 401)
        self.assertIn(
            'Missing Authorization Header', json.loads(response.data)['msg'])

        """Test if an admin can add a book with an access token"""
        # Issue acces token
        access_token = self.register_and_login_admin()
        response = self.test_client.post('/api/v2/books', data=json.dumps({'title': 'Beginning Python', 'author': 'J Wachira',
         'pub_year': '2000'}), headers={'content-type':'application/json', 'authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully added the book  Beginning Python  by author  J Wachira  published in the year 2000', json.loads(response.data)['message'])

        
    def test_user_adding_book(self):
        # Issue access token
        access_token = self.register_and_login_user()

        # Add book with user access token
        response = self.test_client.post('/api/v2/books', data=json.dumps({'name': 'Beginning Python', 'author': 'J Wachira',
         'pub_year': '2000'}), headers={'content-type':'application/json', 'authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 401)
        self.assertEqual('Unauthorized. You need to be an admin to perform this function', json.loads(response.data)['message'])

    def test_getting_all_books(self):
        """Test for retrieving all books"""
        access_token = self.register_and_login_user()
        # Test if user can retrieve all books when the db is empty
        response = self.test_client.get('/api/v2/books', headers={'content-type':'application/json',
         'authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 200)

        
        self.book_1.save_book_to_db()
        self.book_2.save_book_to_db()
        # Try to retrieve all books:
        response = self.test_client.get('/api/v2/books', headers={'content-type':'application/json',
        'authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 200)

    def test_getting_one_book(self):
        access_token = self.register_and_login_user()
        headers={'content-type':'application/json', 'authorization': 'Bearer {}'.format(access_token)}
        # Retrieving an unavailable book:
        response = self.test_client.get('/api/v2/books/12', headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual('There is no book with that ID in the BooksTable', json.loads(response.data)['Message'])
        # Add a new book in order to access it:
        self.book_1.save_book_to_db()
        self.book_2.save_book_to_db()
        # Retrieve added book:
        response = self.test_client.get('/api/v2/books/1', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['Message'], "Book successfully retrieved")

        # Retrieve a book with invalid ID:
        response = self.test_client.get('/api/v2/books/XCGWQU', headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual('Please enter a valid book ID', json.loads(response.data)['Message'])

    def test_admin_deleting_book(self):
        """Test admin deleting a book"""
        # Add a new book:
        access_token = self.register_and_login_admin()
        headers={'content-type':'application/json', 'authorization': 'Bearer {}'.format(access_token)}
        self.book_1.save_book_to_db()
        # Delete book added above:
        response = self.test_client.delete('/api/v2/books/1',  headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(f"You have deleted this book {self.book_1.book_title}", json.loads(response.data)['message'])
        # Try to delete a non-existent book: vb
        response = self.test_client.delete('/api/v2/books/10', headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn("This book does not exist in the library.", json.loads(response.data)['message'])
        
    def test_user_deleting_book(self):
        """Test normal user deleting a book"""
        access_token = self.register_and_login_user()
        headers = {'content-type':'application/json', 'authorization': 'Bearer {}'.format(access_token)}

        # Adding a book
        self.book_1.save_book_to_db()
        # Deleting existing book
        response = self.test_client.delete('/api/v2/books/1',  headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Unauthorized. You need to be an admin to perform this function', json.loads(response.data)['message'])

        # Try to delete a non-existent book
        response = self.test_client.delete('/api/v2/books/10', headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Unauthorized. You need to be an admin to perform this function', json.loads(response.data)['message'])

    def test_updating_book(self):
        """Test admin updating a book"""
        access_token=self.register_and_login_admin()
        headers = {'content-type':'application/json', 'authorization': 'Bearer {}'.format(access_token)}
        # Add a new book:
        self.book_1.save_book_to_db()
        # Update book added above:
        response=self.test_client.put('/api/v2/books/1', data=json.dumps({'name': 'Beginning Javascript 2', 'author': 'M Madam', \
        'pub_year': '2015'}), headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Successfully updated book details', json.loads(response.data)['message'])
        # Try to update a non-existent book
        response=self.test_client.put('/api/v2/books/10', data=json.dumps({'name': 'Beginning Javascript 2', 'author': 'M Madam', \
        'pub_year': '2015'}), headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn("This book does not exist in the library.", json.loads(response.data)['message'])
        # Logout admin to blacklist a token:
        response=self.test_client.post('/api/v2/auth/logout', headers=headers)
       # Try to update a book with blacklisted token:
        response=self.test_client.put('/api/v2/books/1', data=json.dumps({'name': 'Beginning Javascript 2', 'author': 'M Madam', \
        'pub_year': '2015'}), headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual("This token is blacklisted", json.loads(response.data)['message'])


    def tearDown(self):
        """Return to normal state after test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
