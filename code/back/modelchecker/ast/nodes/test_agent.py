# -*- coding: utf-8 -*-
from unittest import TestCase

from modelchecker.ast.nodes import *
from modelchecker.models.KMmodel import KMmodel
from modelchecker import utils


__author__ = 'laura'

class TestAgent(TestCase):
    def setUp(self):
        self.model = KMmodel()
        json_data = utils.read_json('modelchecker/models/test_model_km.json')
        self.model = KMmodel.from_json(json_data)

    def test_is_true_knowledge_1(self):
        # Formula is true
        node = Knowledge(3, Proposition('p'))
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sb'))
        self.assertTrue(truth_value, "The formula is true, there is a reflexive relation.")
        # print dict['condition']
        # print dict['conclusion']
        # print dict['interlude']

    def test_is_true_knowledge_2(self):
        node = Knowledge(1, Proposition('q'))
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sd'))
        self.assertTrue(truth_value, "The agent does not have a relationship in the state.")
        # print dict['conclusion']

    def test_is_true_knowledge_3(self):
        # Formula is false
        node = Knowledge(1, Proposition('p'))
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sd'))
        self.assertTrue(
            truth_value,
            "The formula is false, there no reflexive relation"
        )

    def test_is_true_knowledge_4(self):
        node = Knowledge(1, Proposition('q'))
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sc'))
        self.assertTrue(truth_value, "The agent has only one relationship to a state.")
        # print dict['condition']
        # print dict['conclusion']
        # print dict['interlude']

    def test_is_true_knowledge_5(self):
        node = Knowledge(1, Proposition('r'))
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sc'))
        self.assertFalse(truth_value, "The agent has only one relationship to a state.")
        # print dict['condition']
        # print dict['conclusion']
        # print dict['interlude']


    def test_is_true_knowledge_6(self):
        # Formula is true
        node = Knowledge(3, Proposition('q'))
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sb'))
        self.assertFalse(truth_value, "The formula is true, there is a reflexive relation.")
        # print dict['condition']
        # print dict['conclusion']

    def test_is_true_possible_1(self):
        node = Possible(
            3,
            Negation(
                Conjunction(
                    Proposition('p'),
                    Proposition('q')
                )
            )
        )
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sb'))
        self.assertTrue(truth_value)
        # print dict['condition']
        # print dict['conclusion']


    def test_is_true_possible_2(self):
        node = Possible(
            1,
            Proposition('r')
        )
        (truth_value, dict) = node.is_true(self.model.get_state_by_name('sb'))
        self.assertFalse(truth_value)
        # print dict['condition']
        # print dict['conclusion']


