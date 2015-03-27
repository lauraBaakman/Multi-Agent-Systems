# -*- coding: utf-8 -*-
from unittest import TestCase
from modelchecker.tokenize.tokenizer import tokenize
import modelchecker.operators as operators
from modelchecker.tokenize import tokens
import modelchecker.config as config

__author__ = 'laura'


class TestTokenizeProposition(TestCase):
    def setUp(self):
        self.logics = config.logics

    def test_tokenize_proposition(self):
        expression = 'p'
        for logic in self.logics:
            computed = tokenize(logic, expression)
            expected = [tokens.Proposition('p')]
            self.assertItemsEqual(computed, expected)

    def test_tokenize_conjunction(self):
        expression = 'p & q'
        for logic in self.logics:
            computed = tokenize(logic, expression)
            expected = [
                tokens.Proposition('p'),
                tokens.BinaryOperator(operators.Binary.conjunction),
                tokens.Proposition('q')
            ]
            self.assertEqual(computed, expected)

    def test_tokenize_disjunction(self):
        expression = 'p | q'
        for logic in self.logics:
            computed = tokenize(logic, expression)
            expected = [
                tokens.Proposition('p'),
                tokens.BinaryOperator(operators.Binary.disjunction),
                tokens.Proposition('q')
            ]
            self.assertEqual(computed, expected)

    def test_tokenize_implication(self):
        expression = 'p -> q'
        for logic in self.logics:
            computed = tokenize(logic, expression)
            expected = [
                tokens.Proposition('p'),
                tokens.BinaryOperator(operators.Binary.implication),
                tokens.Proposition('q')
            ]
            self.assertEqual(computed, expected)

    def test_tokenize_biimplication(self):
        expression = 'p <-> q'
        for logic in self.logics:
            computed = tokenize(logic, expression)
            expected = [
                tokens.Proposition('p'),
                tokens.BinaryOperator(operators.Binary.biimplication),
                tokens.Proposition('q')
            ]
            self.assertEqual(computed, expected)

    def test_tokenize_brackets(self):
        expression = '(p & q)'
        for logic in self.logics:
            computed = tokenize(logic, expression)
            expected = [
                tokens.BracketOpen(),
                tokens.Proposition('p'),
                tokens.BinaryOperator(operators.Binary.conjunction),
                tokens.Proposition('q'),
                tokens.BracketClose()
            ]
            self.assertEqual(computed, expected)