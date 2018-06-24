from flask import json, jsonify
import unittest
import os
import sys
sys.path.append('..')
from app import create_app, db
from config import app_config

class AuthorizationTests(unittest.TestCase):
    def setUp(self):
        # """Initialize and define variables for testing."""
        config_name = 'testing'
        self.app = create_app(config_name)
        self.test_client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

        self.user1 = {'name': 'Anabel', 'email': 'anabeladmin@gmail.com', 'password': 'Anabeladm1', 'is_admin': True }
        self.user = {'name': 'Wangui', 'email': 'wangui1@gmail.com', 'password': 'Wangui1' }
        self.upgrade ={'email':'wangui1@gmail.com', 'is_admin': True}
        self.login = {'email': 'anabeladmin@gmail.com', 'password': 'Anabeladm1'}
        self.reset = {'email': 'anabeladmin@gmail.com', 'password': 'newpassword'}
        self.logout = {'email': 'anabeladmin@gmail.com'}
    
    def register_and_login_admin(self):
        # Register a new admin
        self.test_client.post(
            '/api/v2/auth/register', data=json.dumps(self.user1), headers={'content-type':'application/json'})
        
        # Login an admin
        login_response = self.test_client.post(
            '/api/v2/auth/login', data=json.dumps(self.login), headers={'content-type':'application/json'})
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


    def test_creating_user(self):
        #Register an admin
        headers={'content-type':'application/json'}
        response = self.test_client.post('/api/v2/auth/register', data=json.dumps(self.user1), 
            headers=headers)
        self.assertEqual(response.status_code, 201)
        #Register a regular user
        response = self.test_client.post('/api/v2/auth/register', data=json.dumps(self.user), 
            headers=headers)
        self.assertEqual(response.status_code, 201)

    def test_login_user(self):
        headers={'content-type':'application/json'}
        response = self.test_client.post('/api/v2/auth/register', data=json.dumps(self.user1), 
            headers=headers)
        self.assertEqual(response.status_code, 201)
        response = self.test_client.post('/api/v2/auth/login', data=json.dumps(self.login), 
        headers=headers)
        self.assertEqual(response.status_code, 200)
    
    def test_upgrade_user_to_admin(self):
        access_token = self.register_and_login_admin()
        headers={'content-type':'application/json', 'Authorization':'Bearer{}'.format(access_token)}
        self.test_client.post('/api/v2/auth/register', data=json.dumps(self.user), 
            headers={'content-type':'application/json'})
        response = self.test_client.put('/api/v2/auth/register', data=json.dumps(self.upgrade),
        headers=headers)
        self.assertEqual(response.status_code, 200)

        

    
    def test_reset_password_admin(self):
        response = self.test_client.post('/api/v2/auth/register', data=json.dumps(self.user1), 
            headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 201)
        response = self.test_client.post('/api/v2/auth/reset-password', data=json.dumps(self.reset),
        headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 200)
    
    def test_logout_user(self):
        access_token = self.register_and_login_admin()
        headers={'content-type':'application/json', 'Authorization': 'Bearer {}'.format(access_token)}
        response = self.test_client.post('/api/v2/auth/logout', data=json.dumps(self.logout),
            headers=headers)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """Return to normal state after test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ =="__main__":
    unittest.main()