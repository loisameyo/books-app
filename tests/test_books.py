import unittest
from app import app

# from library import app

class BookTests(unittest.TestCase):
    def setUp(self):
        self.app = app()
        self.test_client= self.app.test_client()

    def tearDown(self):
        pass

    def test_creating_book(self):
        response = self.test_client.post('/api/v1/books', content_type='application/json', data={'name': 'python tests'})
        self.assertEqual(response.status, "201 OK")

    def test_getting_book(self):
        self.test_client.post('/api/books', content_type='application/json', data={'name': 'python tests'})
        response = self.test_client.get('/api/v1/books/1')
        self.assertEqual(response.status, "200 Ok")

    def test_deleting_book(self):
        response = self.test_client.post('/api/v1/books', content_type='application/json', data={'name': 'python tests'})
        self.assertEqual(response.status, "200 Ok")
        response = self.test_client.delete('/api/books/1')
        self.assertEqual(response.status, "204 Ok")

    def test_updating_book(self):
        response = self.test_client.post('/api/v1/books', content_type='application/json', data={'name': 'python tests'})
        self.assertEqual(response.status, "200 Ok")
        response = self.test_client.put('/api/books/1', content_type='application/json', data={'name': 'python cookbook', 'borrowed': True})
        self.assertEqual(response.status, "200 Ok")

    def test_creating_user(self):
        response = self.test_client.post('/api/v1/auth/register', content_type='application/json', data={'email': 'loice@gmail.com','passwd':'Loice1', 'logged_in':True})
        self.assertEqual(response.status, "201 OK")
    def test_loggin_user(self):
        response = self.test_client.post('/api/v1/auth/login', content_type='application/json', data={'email': 'loice@gmail.com','passwd':'Loice1'})
        self.assertIsNone(response.status, "201 OK")
        



if __name__== "__main__":
    unittest.main()