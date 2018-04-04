import unittest
from flask import json
from app.__init__ import app

# from library import app

class BookTests(unittest.TestCase):
    def setUp(self):
        self.app = app()
        # self.app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
        self.test_client= self.app.test_client()

    def tearDown(self):
        pass

    def test_creating_book(self):
        response = self.test_client.post('/api/v1/books', data=json.dumps({'name': 'python tests','borrowed': 'False'}), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_getting_book(self):
        response = self.test_client.get('/api/v1/books/1')
        self.assertEqual(response.status_code, 200)

    def test_deleting_book(self):
        response = self.test_client.post('/api/v1/books', data=json.dumps({'name':'python 2','borrowed':'False'}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.test_client.delete('/api/v1/books/1')
        self.assertEqual(response.status_code, 204)

    def test_updating_book(self):
        response = self.test_client.post('/api/v1/books', data=json.dumps({'name':'python tests','borrowed':'False'}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.test_client.put('/api/v1/books/1', data=json.dumps({'name':'python cookbook','borrowed':'True'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_creating_user(self):
        response = self.test_client.post('/api/v1/auth/register', data=json.dumps({'email': 'loice@gmail.com','passwd':'Loice1', 'logged_in':True}), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_loggin_user(self):
        response = self.test_client.post('/api/v1/auth/login', data=json.dumps({'email': 'loice@gmail.com','passwd':'Loice1'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
    def test_loggout_user(self):
        pass

if __name__== "__main__":
    unittest.main()