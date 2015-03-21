# -*- coding: utf-8 -*-
from unittest import TestCase

from modelchecker.ast.nodes import Proposition, Binary, Agent, Unary
from modelchecker.models.kmmodel import KMModel
from modelchecker import operators
from modelchecker import utils


__author__ = 'laura'

class TestAgent(TestCase):
    def setUp(self):
        self.model = KMModel()
        json_data = utils.read_json('modelchecker/models/test_model_km.json')
        self.model = KMModel.from_json(json_data)

    def test_is_true_knowledge_1(self):
        # Formula is true
        node = Agent(operators.Agent.knowledge, 3, Proposition('p'))
        self.assertTrue(
            node.is_true(self.model.get_state_by_name('sb')),
            "The formula is true, there is a reflexive relation."
        )


    def test_is_true_knowledge_2(self):
        node = Agent(operators.Agent.knowledge, 1, Proposition('q'))
        self.assertTrue(
            node.is_true(self.model.get_state_by_name('sd')),
            "The agent does not have a relationship in the state."
        )

    def test_is_true_knowledge_3(self):
        # Formula is false
        node = Agent(operators.Agent.knowledge, 1, Proposition('p'))
        self.assertTrue(
            node.is_true(self.model.get_state_by_name('sc')),
            "The formula is false, there is no reflexive relation"
        )

    def test_is_true_possible_1(self):
        node = Agent(
            operators.Agent.possible,
            3,
            Unary(
                operators.Unary.negation,
                Binary(
                    operators.Binary.conjunction,
                    Proposition('p'),
                    Proposition('q')
                )
            )
        )
        self.assertTrue(
            node.is_true(self.model.get_state_by_name('sb')),
        )

    def test_is_true_possible_2(self):
        node = Agent(
            operators.Agent.possible,
            1,
            Proposition('r')
        )
        self.assertFalse(
            node.is_true(self.model.get_state_by_name('sb')),
        )


