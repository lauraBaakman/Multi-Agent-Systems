# -*- coding: utf-8 -*-
from unittest import TestCase
from modelchecker.tokenize.tokenizer import tokenize
import modelchecker.operators as operators
from modelchecker.tokenize import tokens
import modelchecker.config as config
from modelchecker.errors import  TokenizeError

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

class TestTokenizeK(TestCase):
    def setUp(self):
        self.logics = ['K', 'T', 'S4', 'S5']

    def test_tokenize_K(self):
        expression = 'K_1 p'
        for logic in self.logics:
            computed = tokenize(logic, expression)
            expected = [
                tokens.AgentOperator('1', operators.Agent.knowledge),
                tokens.Proposition('p'),
            ]
            self.assertEqual(computed, expected)

    def test_tokenize_M(self):
        expression = 'M_1 p'
        for logic in self.logics:
            computed = tokenize(logic, expression)
            expected = [
                tokens.AgentOperator('1', operators.Agent.possible),
                tokens.Proposition('p'),
            ]
            self.assertEqual(computed, expected)

    def test_tokenize_C(self):
        expression = 'C p'
        for logic in self.logics:
            self.assertRaises(TokenizeError, tokenize, logic, expression)

    def test_tokenize_E(self):
        expression = 'E p'
        for logic in self.logics:
            self.assertRaises(TokenizeError, tokenize, logic, expression)

    def test_tokenize_I(self):
        expression = 'I p'
        for logic in self.logics:
            self.assertRaises(TokenizeError, tokenize, logic, expression)

class TestTokenizeEC(TestCase):
    def setUp(self):
        self.logics = ['KEC', 'TEC', 'S4EC', 'S5EC']

    def test_tokenize_K(self):
        expression = 'K_1 p'
        for logic in self.logics:
            computed = tokenize(logic, expression)
            expected = [
                tokens.AgentOperator('1', operators.Agent.knowledge),
                tokens.Proposition('p'),
            ]
            self.assertEqual(computed, expected)

    def test_tokenize_M(self):
        expression = 'M_1 p'
        for logic in self.logics:
            computed = tokenize(logic, expression)
            expected = [
                tokens.AgentOperator('1', operators.Agent.possible),
                tokens.Proposition('p'),
            ]
            self.assertEqual(computed, expected)

    def test_tokenize_C(self):
        expression = 'C p'
        for logic in self.logics:
            computed = tokenize(logic, expression)
            expected = [
                tokens.UnaryOperator(operators.Unary.common),
                tokens.Proposition('p'),
            ]
            self.assertEqual(computed, expected)

    def test_tokenize_E(self):
        expression = 'E p'
        for logic in self.logics:
            computed = tokenize(logic, expression)
            expected = [
                tokens.UnaryOperator(operators.Unary.everybody),
                tokens.Proposition('p'),
            ]
            self.assertEqual(computed, expected)

    def test_tokenize_I(self):
        expression = 'I p'
        for logic in self.logics:
            self.assertRaises(TokenizeError, tokenize, logic, expression)

class TestTokenizeI(TestCase):
    def setUp(self):
        self.logics = ['KI', 'TI', 'S4I', 'S5I']

    def test_tokenize_K(self):
        expression = 'K_1 p'
        for logic in self.logics:
            computed = tokenize(logic, expression)
            expected = [
                tokens.AgentOperator('1', operators.Agent.knowledge),
                tokens.Proposition('p'),
            ]
            self.assertEqual(computed, expected)

    def test_tokenize_M(self):
        expression = 'M_1 p'
        for logic in self.logics:
            computed = tokenize(logic, expression)
            expected = [
                tokens.AgentOperator('1', operators.Agent.possible),
                tokens.Proposition('p'),
            ]
            self.assertEqual(computed, expected)

    def test_tokenize_C(self):
        expression = 'C p'
        for logic in self.logics:
            self.assertRaises(TokenizeError, tokenize, logic, expression)

    def test_tokenize_E(self):
        expression = 'E p'
        for logic in self.logics:
            self.assertRaises(TokenizeError, tokenize, logic, expression)

    def test_tokenize_I(self):
        expression = 'I p'
        for logic in self.logics:
            computed = tokenize(logic, expression)
            expected = [
                tokens.UnaryOperator(operators.Unary.implicit),
                tokens.Proposition('p'),
            ]
            self.assertEqual(computed, expected)