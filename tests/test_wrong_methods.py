# from flask import json, jsonify
# import unittest
# import os
# import sys
# sys.path.append('..')

# from app import create_app, db

# class MethodTests(unittest.TestCase):
#     def setUp(self):
#         """Initialize and define variables for testing"""
#         config_name = 'testing'
#         self.app = create_app(config_name)
#         self.test_cient = self.app.test_cient()
#     def test_wrong_endpoint(self):
#         """Test for when api handles a wrong endpoint url"""
#         response = self.test_cient.get('api/v1/books')
#         self.assertEqual(response.status_code, 404)
#         self.assertIn('http://localhost/api/v1/books is not a valid url',\
#         str(response.data), msg="Handles invalid url")
   
#     def test_wrong_request_method(self):
#         """Test for when api handles a wrong request method"""
#         response = self.test_cient.put('api/v2/books')
#         self.assertEqual(response.status_code, 405)
#         self.assertIn('Method PUT is not allowed for this endpoint',\
#         str(response.data), msg="Handles wrong request method")

#     def test_bad_request(self):
#         """Test for when api handles a wrong request method"""
#         response = self.test_cient.put('api/v2/auth/register')
#         self.assertEqual(response.status_code, 400)
#         self.assertIn('Bad request. This method supports JSON requests only',\
#         str(response.data), msg="Handles bad requests")
    
#     def tearDown(self):
#         """Return to normal state after test"""
#         with self.app.app_context():
#             db.session.remove()
#             db.drop_all ()
    
#     if __name__ == '__main__':
#         unittest.main()