# -*- coding: utf-8 -*-
from unittest import TestCase

from models.kmmodel import  KMModel
import utils

__author__ = 'laura'


class TestKMModel(TestCase):

    def setUp(self):
        self.model = KMModel()
        json_data = utils.read_json('.models/test_model_km.json')
        self.model.from_json(json_data)

    def test_get_propositions(self):
        computed_result = self.model.get_propositions()
        expected_result = ['p', 'q', 'r']
        self.assertItemsEqual(expected_result, computed_result)

    def test_is_true_1(self):
        raise NotImplementedError
