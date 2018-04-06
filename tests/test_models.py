import unittest
import unittest
from flask import json, jsonify
import sys
sys.path.append('..')
from app import app



class ModelsTests(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.test_client= self.app.test_client()

    def tearDown(self):
        pass
def test_models_returns_error_message_if_both_args_not_not_strings(self):
        pass
 
