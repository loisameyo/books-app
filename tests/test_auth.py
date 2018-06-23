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

        self.user1= {'name': 'Odi', 'email': 'loice@gmail.com', 'password': 'Loice1', 'is_admin': True }
        self.response = self.test_client.post('/api/v2/auth/register', 
                    data=json.dumps(self.user1),content_type ='application/json')
        response = self.test_client.post('/api/v2/auth/login', 
                    data=json.dumps(self.user1),content_type ='application/json')
        self.token = json.loads(response.data.decode())['access_token']
        self.headers = {'Content-Type':'application/json', 'Authorization':'Bearer {}'.format(self.token)}


    def test_creating_user(self):
        self.assertEqual(self.response.status_code, 201)

    def test_login_user(self):
        response = self.test_client.post('/api/v2/auth/login', data=json.dumps({'email': 'loice@gmail.com','password':'Loice1'}),\
         content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    # def test_reset_password(self):
    #     response = self.test_client.post('/api/v2/auth/login', data=json.dumps({'email': 'loice@gmail.com','password':'Loice1'}),\
    #      content_type='application/json')
    #     response = self.test_client.post('/api/v2/auth/reset-password', data=json.dumps({'email': 'loice@gmail.com','password':'Loice1'}),\
    #      content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    
    # def test_logout_user(self):
    #     pass

    def tearDown(self):
        """Return to normal state after test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()