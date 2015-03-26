# -*- coding: utf-8 -*-
from unittest import TestCase

from modelchecker.ast.nodes import Proposition, Negation, Conjunction, Everybody
from modelchecker.models import KModel
import modelchecker.utils.translators as utils

__author__ = 'laura'


class TestUnary(TestCase):
    def setUp(self):
        self.model = KModel()
        json_data = utils.read_json('modelchecker/models/test_model_km.json')
        self.model = KModel.from_json(json_data)
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
        # print dict['condition']
        # print dict['conclusion']

    def test_is_true_3(self):
        node = Negation(Conjunction(self.lhs, self.lhs))
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sd'))

        self.assertTrue(truth_value)
        # print dict['condition']

class TestEverybody(TestCase):
    def setUp(self):
        self.model = KModel()
        json_data = utils.read_json('modelchecker/models/test_model_km.json')
        self.model = KModel.from_json(json_data)
        self.lhs = Proposition('p')

    def test_no_relations(self):
        node = Everybody(self.lhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sd'))
        self.assertTrue(truth_value)
        # print dict['condition']
        # print dict['conclusion']

    def test_one_relation(self):
        node = Everybody(self.lhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('se'))
        self.assertFalse(truth_value)
        print dict['condition']
        print dict['conclusion']