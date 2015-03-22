# -*- coding: utf-8 -*-
from unittest import TestCase

from modelchecker import ast
import modelchecker.models as models
from utils import *

__author__ = 'laura'


class TestMotivation_to_latex(TestCase):
    def setUp(self):
        self.logic = "KM"
        filename = './modelchecker/models/test_model_km.json'
        data = read_json(filename)
        self.model = models.kmmodel.KMModel.from_json(data)


    def test_motivation_to_latex(self):
        formula = "K_1 ~ a & (b -> d)"
        tree = ast.Ast.from_string(formula, self.logic)
        (_, motivation) = tree.is_true(self.model.states.get("sa"))
        print motivation
        print motivation_to_latex(motivation)