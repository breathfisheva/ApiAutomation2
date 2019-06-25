'''
test csae base class
'''

import time
import unittest
import requests

class ApiServerUnittest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.host = "http://127.0.0.1:7890"
        cls.api_client = requests.Session()

    @classmethod
    def tearDownClass(cls):
        pass
