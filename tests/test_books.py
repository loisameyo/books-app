import unittest
from app import create_app


# from library import app

class BookTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.test_client= self.app.test_client()

    def tearDown(self):
        pass

    def test_creating_book(self):
        response = self.test_client.post('/api/books', content_type='multipart/form-data', data={'name': 'python tests'})
        self.assertEqual(response.status, "201 OK")

    def test_getting_book(self):
        self.test_client.post('/api/books', content_type='multipart/form-data', data={'name': 'python tests'})
        response = self.test_client.get('/api/books/1')
        self.assertEqual(response.status, "200 Ok")

    def test_deleting_book(self):
        response = self.test_client.post('/api/books', content_type='multipart/form-data', data={'name': 'python tests'})
        self.assertEqual(response.status, "200 Ok")
        response = self.test_client.delete('/api/books/1')
        self.assertEqual(response.status, "204 Ok")

    def test_updating_book(self):
        response = self.test_client.post('/api/books', content_type='multipart/form-data', data={'name': 'python tests'})
        self.assertEqual(response.status, "200 Ok")
        response = self.test_client.put('/api/books/1', content_type='multipart/form-data', data={'name': 'python cookbook', 'borrowed': True})
        self.assertEqual(response.status, "200 Ok")
        



if __name__== "__main__":
    unittest.main()