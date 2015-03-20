# -*- coding: utf-8 -*-
from unittest import TestCase

from nodes import Proposition, Binary
from models.kmmodel import KMModel
from tokenize import operators
import utils

__author__ = 'laura'

class TestBinary(TestCase):

    def setUp(self):
        self.model = KMModel()
        json_data = utils.read_json('./models/test_model_km.json')
        self.model = KMModel.from_json(json_data)
        self.lhs = Proposition('p')
        self.rhs = Proposition('q')

    def test_is_true_conjunction(self):
        node = Binary(operators.Binary.conjunction, self.lhs, self.rhs)

        self.assertTrue(node.is_true(self.model.get_state_by_name('sa')))
        self.assertFalse(node.is_true(self.model.get_state_by_name('sb')))
        self.assertFalse(node.is_true(self.model.get_state_by_name('sc')))
        self.assertFalse(node.is_true(self.model.get_state_by_name('sd')))

    def test_is_true_disjunction(self):
        node = Binary(operators.Binary.disjunction, self.lhs, self.rhs)

        self.assertTrue(node.is_true(self.model.get_state_by_name('sa')))
        self.assertTrue(node.is_true(self.model.get_state_by_name('sb')))
        self.assertFalse(node.is_true(self.model.get_state_by_name('sc')))
        self.assertTrue(node.is_true(self.model.get_state_by_name('sd')))

    def test_is_true_implication(self):
        node = Binary(operators.Binary.implication, self.lhs, self.rhs)

        self.assertTrue(node.is_true(self.model.get_state_by_name('sa')))
        self.assertFalse(node.is_true(self.model.get_state_by_name('sb')))
        self.assertTrue(node.is_true(self.model.get_state_by_name('sc')))
        self.assertTrue(node.is_true(self.model.get_state_by_name('sd')))

    def test_is_true_biimplication(self):
        node = Binary(operators.Binary.biimplication, self.lhs, self.rhs)

        self.assertTrue(node.is_true(self.model.get_state_by_name('sa')))
        self.assertFalse(node.is_true(self.model.get_state_by_name('sb')))
        self.assertTrue(node.is_true(self.model.get_state_by_name('sc')))
        self.assertFalse(node.is_true(self.model.get_state_by_name('sd')))


class TestProposition(TestCase):
    def setUp(self):
        self.model = KMModel()
        json_data = utils.read_json('./models/test_model_km.json')
        self.model = KMModel.from_json(json_data)
        pass

    def test_is_true(self):
        node = Proposition('p')
        self.assertTrue(node.is_true(self.model.get_state_by_name('sa')))
        self.assertTrue(node.is_true(self.model.get_state_by_name('sb')))
        self.assertFalse(node.is_true(self.model.get_state_by_name('sc')))

        node = Proposition('q')
        self.assertTrue(node.is_true(self.model.get_state_by_name('sa')))
        self.assertFalse(node.is_true(self.model.get_state_by_name('sb')))
        self.assertFalse(node.is_true(self.model.get_state_by_name('sc')))

        node = Proposition('r')
        self.assertFalse(node.is_true(self.model.get_state_by_name('sa')))
        self.assertTrue(node.is_true(self.model.get_state_by_name('sb')))
        self.assertTrue(node.is_true(self.model.get_state_by_name('sc')))