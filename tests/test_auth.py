from flask import json, jsonify
import unittest
import os
import sys
sys.path.append('..')
from app import create_app, db, mail
from config import app_config

class AuthorizationTests(unittest.TestCase):
    def setUp(self):
        # """Initialize and define variables for testing."""
        config_name = 'testing'
        self.app = create_app(config_name)
        self.test_client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

        self.user1 = {'name': 'Anabel', 'email': 'anabeladmin@gmail.com', 'password': 'Anabeladm1','confirm password': 'Anabeladm1', 'is_admin': True }
        self.user = {'name': 'Wangui', 'email': 'wangui1@gmail.com', 'password': 'Wangui1', 'confirm password': 'Wangui1' }
        self.login = {'email': 'anabeladmin@gmail.com', 'password': 'Anabeladm1'}
        self.user_login={'email': 'wangui1@gmail.com', 'password': 'Wangui1'}
        self.upgrade ={'email':'wangui1@gmail.com'}
        self.reset = {'email': 'wangui1@gmail.com', 'password': 'Wangui1','confirm password':'Wangui2'}
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
            '/api/v2/auth/login', data=json.dumps(self.user_login), headers={'content-type':'application/json'})
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
        # response = self.test_client.put('/api/v2/auth/register', data=json.dumps(self.upgrade),
        # headers=headers)
        # self.assertEqual(response.status_code, 200)

        
    def test_password_reset_for_unregistered_user(self):
        response = self.test_client.post('/api/v2/auth/reset-password', data=json.dumps(self.user_login),
            headers={'content-type': 'application/json'})
        email = self.user_login['email']
        self.assertIn('No user is registered with this address'.format(email), str(response.data))
    def test_password_reset_with_wrong_token(self):
        # Register a user to reset-password
        self.test_client.post('/api/v2/auth/register', data=json.dumps(self.user),
                         headers={'content-type': 'application/json'})
        
        # Reset password by getting sending a token to user email
        with mail.record_messages() as outbox:
            response = self.test_client.post('/api/v2/auth/reset-password', data=json.dumps(self.reset),
            headers={'content-type': 'application/json'})
            self.assertIn('A password reset link has been sent to your email.', str(response.data))
            token = outbox[0].body
            wrong_token = token[::-1]
            # Reset with the wrong token
            response = self.test_client.post(
                '/api/v2/auth/reset-password?token={}'.format(wrong_token),
                data=json.dumps(self.reset),
                headers={'content-type': 'application/json'})
            self.assertIn('nvalid or expired token for the user.',
                          str(response.data))
    # def test_password_reset_with_right_token(self):
    #     self.register_and_login_user()
        
    #     # Reset password by getting sending a token to user email
    #     with mail.record_messages() as outbox:
    #         response = self.test_client.post('/api/v2/auth/reset-password', data=json.dumps(self.reset),
    #             headers={'content-type': 'application/json'})
    #         self.assertIn('A password reset link has been sent to your email.', str(response.data))
    #         token = outbox[0].body
    #         wrong_token = token[::-1]
    #         # Reset with the right token
    #         response = self.test_client.post(
    #             '/api/v2/auth/reset-password?token={}'.format(token), data=json.dumps(self.reset),
    #             headers={'content-type': 'application/json'})
    #         self.assertIn('Reset successful.',str(response.data))
    
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