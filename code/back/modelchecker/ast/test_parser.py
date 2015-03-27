# -*- coding: utf-8 -*-
from unittest import TestCase

from modelchecker.tokenize import tokens
from modelchecker.ast.ast import Ast
from modelchecker.ast import nodes

__author__ = 'laura'


class TestParser(TestCase):
    def setUp(self):
        self.p = tokens.Proposition("p")
        self.q = tokens.Proposition("q")

    def test_parse_proposition(self):
        computed_tree = Ast.from_string("p", "KM").root
        expected_tree = nodes.Proposition("p")
        self.assertEqual(computed_tree, expected_tree)

    def test_parse_conjunction(self):
        computed_tree = Ast.from_string("p & q", "KM").root
        expected_tree = nodes.Conjunction(
            nodes.Proposition("p"),
            nodes.Proposition("q")
        )
        self.assertEqual(computed_tree, expected_tree)

    def test_parse_disjunction(self):
        computed_tree = Ast.from_string("p | q", "KM").root
        expected_tree = nodes.Disjunction(
            nodes.Proposition("p"),
            nodes.Proposition("q")
        )
        self.assertEqual(computed_tree, expected_tree)

    def test_parse_implication(self):
        computed_tree = Ast.from_string("p -> q", "KM").root
        expected_tree = nodes.Implication(
            nodes.Proposition("p"),
            nodes.Proposition("q")
        )
        self.assertEqual(computed_tree, expected_tree)

    def test_parse_biimplication(self):
        computed_tree = Ast.from_string("p <-> q", "KM").root
        expected_tree = nodes.BiImplication(
            nodes.Proposition("p"),
            nodes.Proposition("q")
        )
        self.assertEqual(computed_tree, expected_tree)

    def test_parse_negation(self):
        computed_tree = Ast.from_string("~ p", "KM").root
        expected_tree = nodes.Negation(
            nodes.Proposition("p")
        )
        self.assertEqual(computed_tree, expected_tree)

    def test_parse_common(self):
        computed_tree = Ast.from_string("C p", "KEC").root
        expected_tree = nodes.Common(
            nodes.Proposition("p")
        )
        self.assertEqual(computed_tree, expected_tree)

    def test_parse_everybody(self):
        computed_tree = Ast.from_string("E p", "KEC").root
        expected_tree = nodes.Everybody(
            nodes.Proposition("p")
        )
        self.assertEqual(computed_tree, expected_tree)

    def test_parse_knowledge(self):
        computed_tree = Ast.from_string("K_1 p", "KM").root
        expected_tree = nodes.Knowledge(
            "1",
            nodes.Proposition("p")
        )
        self.assertEqual(computed_tree, expected_tree)

    def test_parse_possible(self):
        computed_tree = Ast.from_string("M_1 p", "KM").root
        expected_tree = nodes.Possible(
            "1",
            nodes.Proposition("p")
        )
        self.assertEqual(computed_tree, expected_tree)

    def test_parse_intention(self):
        computed_tree = Ast.from_string("I p", "KI").root
        expected_tree = nodes.Implicit(
            nodes.Proposition("p")
        )
        self.assertEqual(computed_tree, expected_tree)