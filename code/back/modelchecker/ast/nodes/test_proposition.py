# -*- coding: utf-8 -*-
from unittest import TestCase

from modelchecker.models.KMmodel import KMmodel
from modelchecker import utils
from modelchecker.ast.nodes import Proposition

__author__ = 'laura'


class TestProposition(TestCase):
    def setUp(self):
        self.model = KMmodel()
        json_data = utils.read_json('./modelchecker/models/test_model_km.json')
        self.model = KMmodel.from_json(json_data)

    def test_is_true_true(self):
        node = Proposition('p')
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sa'))
        self.assertTrue(truth_value)
        # print dict


    def test_is_true_false(self):
        node = Proposition('p')
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sc'))
        self.assertFalse(truth_value)
        # print dict