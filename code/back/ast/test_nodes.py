# -*- coding: utf-8 -*-
from unittest import TestCase

from nodes import Binary, Proposition
from models.kmmodel import KMModel
from tokenize import operators, tokens
import utils

__author__ = 'laura'

import models.errors as errors

class TestBinary(TestCase):
    def setUp(self):
        self.model = KMModel()
        json_data = utils.read_json('./models/test_model_km.json')
        self.model = KMModel.from_json(json_data)
        self.lhs = Proposition(tokens.Proposition('p'))
        self.rhs = Proposition(tokens.Proposition('q'))

    def test_is_true_conjunction(self):
        node = Binary(
            tokens.BinaryOperator(
                operators.Binary.conjunction
            )
        )
        node.lhs = self.lhs
        node.rhs = self.rhs

        self.assertTrue(node.is_true(self.model, self.model.get_state_by_name('sa')))
        self.assertFalse(node.is_true(self.model, self.model.get_state_by_name('sb')))
        self.assertFalse(node.is_true(self.model, self.model.get_state_by_name('sc')))
        self.assertFalse(node.is_true(self.model, self.model.get_state_by_name('sd')))

    def test_is_true_disjunction(self):
        node = Binary(
            tokens.BinaryOperator(
                operators.Binary.disjunction
            )
        )
        node.lhs = self.lhs
        node.rhs = self.rhs

        self.assertTrue(node.is_true(self.model, self.model.get_state_by_name('sa')))
        self.assertTrue(node.is_true(self.model, self.model.get_state_by_name('sb')))
        self.assertFalse(node.is_true(self.model, self.model.get_state_by_name('sc')))
        self.assertTrue(node.is_true(self.model, self.model.get_state_by_name('sd')))

    def test_is_true_implication(self):
        node = Binary(
            tokens.BinaryOperator(
                operators.Binary.implication
            )
        )
        node.lhs = self.lhs
        node.rhs = self.rhs

        self.assertTrue(node.is_true(self.model, self.model.get_state_by_name('sa')))
        self.assertFalse(node.is_true(self.model, self.model.get_state_by_name('sb')))
        self.assertTrue(node.is_true(self.model, self.model.get_state_by_name('sc')))
        self.assertTrue(node.is_true(self.model, self.model.get_state_by_name('sd')))

    def test_is_true_biimplication(self):
        node = Binary(
            tokens.BinaryOperator(
                operators.Binary.biimplication
            )
        )
        node.lhs = self.lhs
        node.rhs = self.rhs

        self.assertTrue(node.is_true(self.model, self.model.get_state_by_name('sa')))
        self.assertFalse(node.is_true(self.model, self.model.get_state_by_name('sb')))
        self.assertTrue(node.is_true(self.model, self.model.get_state_by_name('sc')))
        self.assertFalse(node.is_true(self.model, self.model.get_state_by_name('sd')))


class TestProposition(TestCase):
    def setUp(self):
        self.model = KMModel()
        json_data = utils.read_json('./models/test_model_km.json')
        self.model = KMModel.from_json(json_data)
        pass

    def test_is_true(self):
        node = Proposition(tokens.Proposition('p'))
        self.assertTrue(node.is_true(self.model.get_state_by_name('sa')))
        self.assertTrue(node.is_true(self.model.get_state_by_name('sb')))
        self.assertFalse(node.is_true(self.model.get_state_by_name('sc')))

        node = Proposition(tokens.Proposition('q'))
        self.assertTrue(node.is_true(self.model.get_state_by_name('sa')))
        self.assertFalse(node.is_true(self.model.get_state_by_name('sb')))
        self.assertFalse(node.is_true(self.model.get_state_by_name('sc')))

        node = Proposition(tokens.Proposition('r'))
        self.assertFalse(node.is_true(self.model.get_state_by_name('sa')))
        self.assertTrue(node.is_true(self.model.get_state_by_name('sb')))
        self.assertTrue(node.is_true(self.model.get_state_by_name('sc')))