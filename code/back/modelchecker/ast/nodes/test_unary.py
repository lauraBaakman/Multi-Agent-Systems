# -*- coding: utf-8 -*-
from unittest import TestCase

from modelchecker.ast.nodes import Proposition, Negation
from modelchecker.models.kmmodel import KMModel
from modelchecker import utils

__author__ = 'laura'


class TestUnary(TestCase):
    def setUp(self):
        self.model = KMModel()
        json_data = utils.read_json('modelchecker/models/test_model_km.json')
        self.model = KMModel.from_json(json_data)
        self.lhs = Proposition('p')

    def test_is_true_1(self):
        node = Negation(self.lhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sa'))

        self.assertFalse(truth_value)
        # print dict['condition'] + '\\\\'
        # print dict['conclusion']

    def test_is_true_2(self):
        node = Negation(self.lhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sd'))

        self.assertTrue(truth_value)
        # print dict['condition'] + '\\\\'
        # print dict['conclusion']