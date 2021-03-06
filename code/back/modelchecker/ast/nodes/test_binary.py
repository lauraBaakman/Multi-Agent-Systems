# -*- coding: utf-8 -*-
from unittest import TestCase

__author__ = 'laura'
from modelchecker.ast.nodes import Proposition, Conjunction, Disjunction, Implication, BiImplication
from modelchecker.models import KModel
import modelchecker.utils.translators as utils

class TestBinary(TestCase):
    def setUp(self):
        self.model = KModel()
        json_data = utils.read_json('modelchecker/models/test_model_km.json')
        self.model = KModel.from_json(json_data)
        self.lhs = Proposition('p')
        self.rhs = Proposition('q')

    def test_is_true_conjunction_1(self):
        node = Conjunction(self.lhs, self.rhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sa'))

        self.assertTrue(truth_value)
        # print dict['condition'] + '\\\\'
        # print dict['conclusion']

    def test_is_true_conjunction_2(self):
        node = Conjunction(self.lhs, self.rhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sb'))

        self.assertFalse(truth_value)
        # print dict['condition'] + '\\\\'
        # print dict['conclusion']

    def test_is_true_conjunction_3(self):
        node = Conjunction(self.lhs, self.rhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sc'))

        self.assertFalse(truth_value)
        # print dict['condition'] + '\\\\'
        # print dict['conclusion']

    def test_is_true_conjunction_4(self):
        node = Conjunction(self.lhs, self.rhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sd'))

        self.assertFalse(truth_value)
        # print dict['condition'] + '\\\\'
        # print dict['conclusion']


    def test_is_true_disjunction_1(self):
        node = Disjunction(self.lhs, self.rhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sa'))

        self.assertTrue(truth_value)
        # print dict['interlude']
        # print dict['condition'] + '\\\\'
        # print dict['conclusion']

    def test_is_true_disjunction_2(self):
        node = Disjunction(self.lhs, self.rhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sb'))

        self.assertTrue(truth_value)
        # print dict['interlude']
        # print dict['condition'] + '\\\\'
        # print dict['conclusion']

    def test_is_true_disjunction_3(self):
        node = Disjunction(self.lhs, self.rhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sc'))

        self.assertFalse(truth_value)
        # print dict['interlude']
        # print dict['condition'] + '\\\\'
        # print dict['conclusion']

    def test_is_true_disjunction_4(self):
        node = Disjunction(self.lhs, self.rhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sd'))

        self.assertTrue(truth_value)
        # print dict['interlude']
        # print dict['condition'] + '\\\\'
        # print dict['conclusion']


    def test_is_true_implication_1(self):
        node = Implication(self.lhs, self.rhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sd'))

        self.assertTrue(truth_value)
        # print dict['condition'] + '\\\\\n'
        # print dict['conclusion']

    def test_is_true_implication_2(self):
        node = Implication(self.lhs, self.rhs)
        (truth_value, _) = node.is_true(self.model.get_state_by_name('sb'))
        self.assertFalse(truth_value)

    def test_is_true_implication_3(self):
        node = Implication(self.lhs, self.rhs)
        (truth_value, _) = node.is_true(self.model.get_state_by_name('sc'))
        self.assertTrue(truth_value)

    def test_is_true_implication_4(self):
        node = Implication(self.lhs, self.rhs)
        (truth_value, _) = node.is_true(self.model.get_state_by_name('sa'))
        self.assertTrue(truth_value)

    def test_is_true_biimplication_1(self):
        node = BiImplication(self.lhs, self.rhs)
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sa'))
        self.assertTrue(truth_value)
        # print dict['condition'] + '\\\\'
        # print dict['conclusion'] + '\\\\'
        # print dict['interlude']

    def test_is_true_biimplication_2(self):
        node = BiImplication(self.lhs, self.rhs)
        (truth_value, _) = node.is_true(self.model.get_state_by_name('sb'))
        self.assertFalse(truth_value)