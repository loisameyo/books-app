from flask import json, jsonify
import unittest
import os
import sys
sys.path.append('..')
from app import app



class EndpointTests(unittest.TestCase):
    def setUp(self):
        """Initialize and define variables for testing."""
        config_name = 'testing'
        self.app = app(config_name)
        self.test_client = self.app.test_client()

    
    def register_and_login_admin(self):
        # Register a new admin
        self.test_test_client.post('/api/v2/auth/register', data=json.dumps({'name':'Odi','email':'loice@gmail.com','password':'Loice1','is_admin':True}),\
         content_type='application/json')

        # Login an admin
        login_response = self.test_client.post(
            '/api/v2/auth/login', data=json.dumps({'email': 'loiceadmin@gmail.com','password':'AdmLoice1'}),\
            content_type='application/json')
        # Get admin access token
        access_token = json.loads(
            login_response.get_data().decode('utf-8'))['access_token']

        return access_token

    def register_and_login_user(self):
        # Register a new user
        self.test_client.post('/api/v2/auth/register', data=json.dumps({'email': 'loice@gmail.com','password':'Loice1'}),\
         content_type='application/json')

        # Login a user
        login_response = self.test_client.post(
            '/api/v2/auth/login', data=json.dumps({'email': 'loice@gmail.com','password':'Loice1'}),\
         content_type='application/json')
        # Get user access token
        access_token = json.loads(
            login_response.get_data().decode('utf-8'))['access_token']

        return access_token

    def test_admin_adding_book(self):
        """Test if an admin can add a book without an access token"""
        response = self.test_client.post('/api/v2/books', data=json.dumps({'name': 'Beginning Python', 'author': 'J Wachira', \
         'pub_year':'2000'}), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Unauthorized. Cannot add book without access token',str(response.data))

        """Test if an admin can add a book with an access token"""
        #Issue acces token
        access_token = self.register_and_login_admin()
        response = self.test_client.post('/api/v2/books', data=json.dumps({'name': 'Beginning Python', 'author': 'J Wachira', \
         'pub_year':'2000', 'authorization :Bearer {}'.format(access_token)}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully added this book', str(response.data))

        """Test against adding a book twice"""
        response = self.test_client.post('/api/v2/books', data=json.dumps({'name': 'Beginning Python', 'author': 'J Wachira', \
         'pub_year':'2000', 'authorization :Bearer {}'.format(access_token)}), content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertIn('This book already exists', str(response.data))

    def test_user_adding_book(self):
        # Issue access token
        access_token = self.register_login_user()

        # Add book with user access token
        response = self.test_client.post('/api/v2/books', data=json.dumps({'name': 'Beginning Python', 'author': 'J Wachira', \
         'pub_year':'2000', 'authorization :Bearer {}'.format(access_token)}), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Unauthorized. You need to be an admin add a continue.',str(response.data))



    def test_getting_all_books(self):
        response = self.test_client.get('/api/v2/books')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Beginning French', str(response.data))

    def test_getting_one_book(self):
        response = self.test_client.get('/api/v2/books/1')
        self.assertEqual(response.status_code, 200)
        #self.assertIn(1, (response.data))

    def test_admin_deleting_book(self):
        """Test admin deleting a book"""

        access_token = self.register_and_login_admin()
        #Add a new book:
        response = self.test_client.post('/api/v2/books', data=json.dumps({'name': 'Beginning Javascript', 'author': 'M Madam', \
        'pub_year':'2015','authorization :Bearer {}'.format(access_token)}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        #Delete book added above:
        response = self.test_client.delete('/api/v2/books/1', data=json.dumps({'name': 'Beginning Javascript', 'author': 'M Madam', \
        'pub_year':'2015','authorization :Bearer {}'.format(access_token)}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Book deleted successfully,", str(response.data))
        #Try to delete a non-existent book:
        response = self.test_client.delete('/api/v2/books/10', data=json.dumps({'name': 'Beginning Javascript', 'author': 'M Madam', \
        'pub_year':'2015','authorization :Bearer {}'.format(access_token)}), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn("No book with this ID,", str(response.data))
        #Try to delete a book with invalid ID:
        response = self.test_client.delete('/api/v2/books/JHYXG', data=json.dumps({'name': 'Beginning Javascript', 'author': 'M Madam', \
        'pub_year':'2015','authorization :Bearer {}'.format(access_token)}), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Invalid book ID,", str(response.data))

    def test_user_deleting_book(self):
        """Test normal user deleting a book"""
       access_token = self.register_login_user()
       
        #Adding a book
        response = self.test_client.post('/api/v2/books', data=json.dumps({'name': 'Beginning Python', 'author': 'J Wachira', \
         'pub_year':'2000', 'authorization :Bearer {}'.format(access_token)}), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Unauthorized. You need to be an admin add a continue.',str(response.data))
        
        #Deleting existing book
        response = self.test_client.delete('/api/v2/books/1', data=json.dumps({'name': 'Beginning Javascript', 'author': 'M Madam', \
        'pub_year':'2015','authorization :Bearer {}'.format(access_token)}), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Unauthorized. You need to be an admin add a continue.',str(response.data)
        
        #Try to delete a non-existent book:
        response = self.test_client.delete('/api/v2/books/10', data=json.dumps({'name': 'Beginning Javascript', 'author': 'M Madam', \
        'pub_year':'2015','authorization :Bearer {}'.format(access_token)}), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Unauthorized. You need to be an admin add a continue.',str(response.data))
       
        
        #Try to delete a book with invalid ID:
        response = self.test_client.delete('/api/v2/books/JHYXG', data=json.dumps({'name': 'Beginning Javascript', 'author': 'M Madam', \
        'pub_year':'2015','authorization :Bearer {}'.format(access_token)}), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Unauthorized. You need to be an admin add a continue.',str(response.data)



    def test_updating_book(self):
        """Test admin updating a book"""
        access_token = self.register_and_login_admin()
        
        #Add a new book:
        response = self.test_client.post('/api/v2/books', data=json.dumps({'name': 'Beginning Javascript 2', 'author': 'M Madam', \
        'pub_year':'2015','authorization :Bearer {}'.format(access_token)}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        #Delete book added above:
        response = self.test_client.put('/api/v2/books/1', data=json.dumps({'name': 'Beginning Javascript 2', 'author': 'M Madam', \
        'pub_year':'2015','authorization :Bearer {}'.format(access_token)}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Book deleted successfully,", str(response.data))
        #Try to delete a non-existent book:
        response = self.test_client.put('/api/v2/books/10', data=json.dumps({'name': 'Beginning Javascript 2', 'author': 'M Madam', \
        'pub_year':'2015','authorization :Bearer {}'.format(access_token)}), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn("No book with this ID,", str(response.data))
        #Try to delete a book with invalid ID:
        response = self.test_client.put('/api/v2/books/JHYXG', data=json.dumps({'name': 'Beginning Javascript 2', 'author': 'M Madam', \
        'pub_year':'2015','authorization :Bearer {}'.format(access_token)}), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Invalid book ID,", str(response.data))
        #Logout admin to blacklist a token:
        response = self.test_client.post('/api/v2/auth/logout',\
         data=json.dumps({'email': 'loiceadmin@gmail.com','password':'AdmLoice1', 'authorization :Bearer {}'.format(access_token)}),\
            content_type='application/json')
        
        #Try to update a book with blacklisted token:
        response = self.test_client.put('/api/v2/books/1', data=json.dumps({'name': 'Beginning Javascript 2', 'author': 'M Madam', \
        'pub_year':'2015','authorization :Bearer {}'.format(access_token)}), content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertIn("The token has been blacklisted,", str(response.data))


        
    
    # def test_borrowing_book(self):
    #      response = self.test_client.post('/api/v1/books', data=json.dumps({'name': 'Beginning French', 'author': 'S Gitau', \
    #      'pub_year':'2000'}), content_type='application/json')
    #      self.assertEqual(response.status_code, 201)
    #      response = self.test_client.post('/api/v1/users/books/1')
    #      self.assertEqual(response.status_code, 200)
    #      #self.assertIn('Book successfully borrowed', str(response.data))

    # def test_creating_user(self):
    #     response = self.test_client.post('/api/v1/auth/register', data=json.dumps({'email': 'loice@gmail.com','password':'Loice1'}),\
    #      content_type='application/json')
    #     self.assertEqual(response.status_code, 201)

    # def test_login_user(self):
    #     response = self.test_client.post('/api/v1/auth/login', data=json.dumps({'email': 'loice@gmail.com','password':'Loice1'}),\
    #      content_type='application/json')
    #     self.assertEqual(response.status_code, 201)
    
    # def test_reset_password(self):
    #     response = self.test_client.post('/api/v1/auth/login', data=json.dumps({'email': 'loice@gmail.com','password':'Loice1'}),\
    #      content_type='application/json')
    #     response = self.test_client.post('/api/v1/auth/reset-password', data=json.dumps({'email': 'loice@gmail.com','password':'Loice1'}),\
    #      content_type='application/json')
    #     self.assertEqual(response.status_code, 201)
    
    # def test_logout_user(self):
    #     pass

def tearDown(self):
     def tearDown(self):
        """Return to normal state after test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        pass

if __name__== "__main__":
    unittest.main()