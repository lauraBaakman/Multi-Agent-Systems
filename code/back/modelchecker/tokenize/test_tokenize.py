# -*- coding: utf-8 -*-
from unittest import TestCase
from modelchecker.tokenize.tokenizer import tokenize
import modelchecker.operators as operators
from modelchecker.tokenize import tokens

__author__ = 'laura'


class TestTokenizeKM(TestCase):
    def test_tokenize_proposition(self):
        logic = 'KM'
        expression = 'p'
        computed = tokenize(logic, expression)
        expected = [tokens.Proposition('p')]
        self.assertEqual(computed, expected)