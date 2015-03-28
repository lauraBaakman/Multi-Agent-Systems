# -*- coding: utf-8 -*-

__author__ = 'laura'
from unittest import TestCase
import modelchecker.config as config
import requests

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

    def test_post_ok(self):
         # TODO: Check of de response de verwachte elementen bevat.
        raise NotImplementedError

    def test_post_error(selfs):
        # TODO: Test of er bij een fout model  een error gegenereerd wordt.Niet alle gevallent testen.
        raise NotImplementedError