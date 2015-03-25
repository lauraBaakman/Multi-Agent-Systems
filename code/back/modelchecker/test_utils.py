# -*- coding: utf-8 -*-
from unittest import TestCase

from modelchecker import ast
import modelchecker.models as models
from modelchecker.utils import *
import os

__author__ = 'laura'


class TestMotivation_to_latex(TestCase):
    def setUp(self):
        self.logic = "KM"
        filename = './modelchecker/models/test_model_km.json'
        data = read_json(filename)
        self.model = models.kmmodel.KMModel.from_json(data)


    def test_motivation_to_latex_negation(self):
        formula = "~ p"
        tree = ast.Ast.from_string(formula, self.logic)
        (_, motivation) = tree.is_true(self.model.states.get("sa"))
        # print motivation_to_latex(motivation)

    def test_motivation_to_latex_conjunction(self):
        formula = "p & q & r"
        tree = ast.Ast.from_string(formula, self.logic)
        (_, motivation) = tree.is_true(self.model.states.get("sa"))
        # print motivation_to_latex(motivation)

    def test_motivation_to_latex_disjunction(self):
        formula = "p | q & r"
        tree = ast.Ast.from_string(formula, self.logic)
        (_, motivation) = tree.is_true(self.model.states.get("sa"))
        # print motivation_to_latex(motivation)

    def test_motivation_to_latex_implication(self):
        formula = "p -> q"
        tree = ast.Ast.from_string(formula, self.logic)
        (_, motivation) = tree.is_true(self.model.states.get("sa"))
        # print motivation_to_latex(motivation)

    def test_motivation_to_latex_biimplication(self):
        formula = "p <-> q"
        tree = ast.Ast.from_string(formula, self.logic)
        (_, motivation) = tree.is_true(self.model.states.get("sa"))
        # print motivation_to_latex(motivation)

    def test_motivation_to_latex_knowledge(self):
        formula = "K_1 p"
        tree = ast.Ast.from_string(formula, self.logic)
        (_, motivation) = tree.is_true(self.model.states.get("sa"))
        # print motivation_to_latex(motivation)

    def test_motivation_to_latex_possible(self):
        formula = "K_2 q & (p | r)"
        tree = ast.Ast.from_string(formula, self.logic)
        (_, motivation) = tree.is_true(self.model.states.get("sc"))
        print motivation_to_latex(motivation)