import unittest
import unittest
from flask import json, jsonify
import sys
sys.path.append('..')
from app import app
from app.models import Books, Users



class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.test_client= app

    def tearDown(self):
        pass

    def test_sub_class(self):
        self.assertFalse(issubclass(Users, Books), msg='Not True subclass of Users Class.')


  