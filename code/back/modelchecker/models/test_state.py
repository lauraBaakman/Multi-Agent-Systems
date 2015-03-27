# -*- coding: utf-8 -*-
from unittest import TestCase

__author__ = 'laura'

import modelchecker.models as models
import modelchecker.utils.translators as translators
import modelchecker.errors as errors

class TestState(TestCase):
    def setUp(self):
        filename = './modelchecker/models/test_model_km.json'
        data = translators.read_json(filename)
        self.model = models.KModel.from_json(data)

    def test_get_all_outgoing_as_two_tuple_1(self):
        state = self.model.get_state_by_name('sd')
        computed = state.get_all_outgoing_as_two_tuple()
        expected = set()
        self.assertEqual(computed, expected)

    def test_get_all_outgoing_as_two_tuple_2(self):
        state = self.model.get_state_by_name('se')
        computed = [(source.name, destination.name) for (source, destination) in state.get_all_outgoing_as_two_tuple()]
        expected = {('se', 'se')}
        self.assertItemsEqual(computed, expected)

    def test_get_all_outgoing_as_two_tuple_3(self):
        state = self.model.get_state_by_name('sa')
        computed = [(source.name, destination.name) for (source, destination) in state.get_all_outgoing_as_two_tuple()]
        expected = {('sa', 'sa'), ('sa','sb'), ('sa', 'sf')}
        self.assertItemsEqual(computed, expected)

    def test_get_all_outgoing_as_two_tuple__with_agent_1(self):
        state = self.model.get_state_by_name('sa')
        self.assertRaises(errors.ModelError, state.get_all_outgoing_as_two_tuple, 'nonExistentAgent')

    def test_get_all_outgoing_as_two_tuple__with_agent_2(self):
        state = self.model.get_state_by_name('sc')
        agent = '2'
        computed = [(source.name, destination.name) for (source, destination) in state.get_all_outgoing_as_two_tuple(agent)]
        expected = {('sc', 'sb'), ('sc', 'sc')}
        self.assertItemsEqual(computed, expected)

    def test_get_all_outgoing_as_two_tuple__with_agent_3(self):
        state = self.model.get_state_by_name('sd')
        agent = '2'
        computed = [(source.name, destination.name) for (source, destination) in
                    state.get_all_outgoing_as_two_tuple(agent)]
        expected = set([])
        self.assertItemsEqual(computed, expected)


