# -*- coding: utf-8 -*-
from unittest import TestCase

__author__ = 'laura'
from modelchecker.ast.nodes import Proposition, Binary
from modelchecker.models.kmmodel import KMModel
from modelchecker import operators
from modelchecker import utils

class TestBinary(TestCase):
    def setUp(self):
        self.model = KMModel()
        json_data = utils.read_json('modelchecker/models/test_model_km.json')
        self.model = KMModel.from_json(json_data)
        self.lhs = Proposition('p')
        self.rhs = Proposition('q')

    def test_is_true_conjunction_1(self):
        node = Binary(operators.Binary.conjunction, self.lhs, self.rhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sa'))

        self.assertTrue(truth_value)
        # print dict['condition'] + '\\\\'
        # print dict['conclusion']

    def test_is_true_conjunction_2(self):
        node = Binary(operators.Binary.conjunction, self.lhs, self.rhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sb'))

        self.assertFalse(truth_value)
        # print dict['condition'] + '\\\\'
        # print dict['conclusion']

    def test_is_true_conjunction_3(self):
        node = Binary(operators.Binary.conjunction, self.lhs, self.rhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sc'))

        self.assertFalse(truth_value)
        # print dict['condition'] + '\\\\'
        # print dict['conclusion']

    def test_is_true_conjunction_4(self):
        node = Binary(operators.Binary.conjunction, self.lhs, self.rhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sd'))

        self.assertFalse(truth_value)
        # print dict['condition'] + '\\\\'
        # print dict['conclusion']


    def test_is_true_disjunction_1(self):
        node = Binary(operators.Binary.disjunction, self.lhs, self.rhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sa'))

        self.assertTrue(truth_value)
        # print dict['condition'] + '\\\\'
        # print dict['conclusion']

    def test_is_true_disjunction_2(self):
        node = Binary(operators.Binary.disjunction, self.lhs, self.rhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sb'))

        self.assertTrue(truth_value)
        # print dict['condition'] + '\\\\'
        # print dict['conclusion']

    def test_is_true_disjunction_3(self):
        node = Binary(operators.Binary.disjunction, self.lhs, self.rhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sc'))

        self.assertFalse(truth_value)
        # print dict['condition'] + '\\\\'
        # print dict['conclusion']

    def test_is_true_disjunction_4(self):
        node = Binary(operators.Binary.disjunction, self.lhs, self.rhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sd'))

        self.assertTrue(truth_value)
        print dict['condition'] + '\\\\'
        print dict['conclusion']


    # def test_is_true_implication(self):
    #     node = Binary(operators.Binary.implication, self.lhs, self.rhs)
    #
    #     self.assertTrue(node.is_true(self.model.get_state_by_name('sa')))
    #     self.assertFalse(node.is_true(self.model.get_state_by_name('sb')))
    #     self.assertTrue(node.is_true(self.model.get_state_by_name('sc')))
    #     self.assertTrue(node.is_true(self.model.get_state_by_name('sd')))
    #
    # def test_is_true_biimplication(self):
    #     node = Binary(operators.Binary.biimplication, self.lhs, self.rhs)
    #
    #     self.assertTrue(node.is_true(self.model.get_state_by_name('sa')))
    #     self.assertFalse(node.is_true(self.model.get_state_by_name('sb')))
    #     self.assertTrue(node.is_true(self.model.get_state_by_name('sc')))
    #     self.assertFalse(node.is_true(self.model.get_state_by_name('sd')))