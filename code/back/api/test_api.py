# -*- coding: utf-8 -*-

__author__ = 'laura'
from unittest import TestCase
import requests

import modelchecker.config as config
import modelchecker.utils.translators as utils


url = 'http://127.0.0.1:8000'

class TestLogics(TestCase):
    def setUp(self):
        self.url = '{url}/logics'.format(url=url)

    def test_get_ok(self):
        response = requests.get(url=self.url)
        self.assertEqual(response.status_code, 200)
        self.assertItemsEqual(
            response.json()['logics'],
            config.logics
        )

class TestValuate(TestCase):
    def setUp(self):
        self.url = '{url}/valuate'.format(url=url)
        self.request_data = utils.read_json('./api/test_request.json')

    def test_post_ok(self):
        response = requests.post(
             url=self.url,
             json=self.request_data
         )
        self.assertEqual(response.status_code, 202)