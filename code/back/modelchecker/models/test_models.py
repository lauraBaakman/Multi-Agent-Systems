# -*- coding: utf-8 -*-
from unittest import TestCase, skip

import modelchecker.utils.translators as translators
import modelchecker.models as models

__author__ = 'laura'


def relations_to_list_of_string_tuples(relations):
    relations_as_tuples = [relation.to_tuple() for relation in relations]
    return [
        (source.name, destination.name, agent)
        for (source, destination, agent) in relations_as_tuples
    ]


def flatten(l):
    return [item for sublist in l for item in sublist]

class TestKMModel(TestCase):
    def setUp(self):
        filename = './modelchecker/models/test_model_km.json'
        data = translators.read_json(filename)
        self.model = models.KModel.from_json(data)

    def test_states(self):
        self.assertItemsEqual(
            self.model.states.keys(),
            ['sa', 'sb', 'sc', 'sd', 'se', 'sf'],
            'Test if all states from the model are in the list of states.'
        )

    def test_agent_set(self):
        computed = self.model.agents
        expected = {'1', '2', '3'}
        self.assertItemsEqual(computed, expected)

    def test_all_states_reachable_from_1(self):
        computed = [
            state.name
            for state in self.model.all_states_reachable_from(self.model.get_state_by_name('sa'))
        ]
        expected = ['sb', 'sa', 'sc', 'sf']
        self.assertItemsEqual(computed, expected)

    def test_all_states_reachable_from_2(self):
        computed = [
            state.name
            for state in self.model.all_states_reachable_from(self.model.get_state_by_name('sd'))
        ]
        expected = ['sd']
        self.assertItemsEqual(computed, expected)

    def test_all_states_reachable_from_3(self):
        computed = [
            state.name
            for state in self.model.all_states_reachable_from(self.model.get_state_by_name('se'))
        ]
        expected = []
        self.assertItemsEqual(computed, expected)

    def test_all_states_reachable_from_4(self):
        computed = [
            state.name
            for state in self.model.all_states_reachable_from(self.model.get_state_by_name('sf'))
        ]
        expected = []
        self.assertItemsEqual(computed, expected)

class TestTModel(TestCase):
    def setUp(self):
        filename = './modelchecker/models/test_model_t.json'
        data = translators.read_json(filename)
        self.model = models.TModel.from_json(data)

    def test_reflexive_closure(self):
        relations_as_tuples = [
            relations_to_list_of_string_tuples(relations)
            for (_, relations) in self.model.relations.iteritems()
        ]
        relations_as_tuples = flatten(relations_as_tuples)
        expected_relations = [('sa', 'sa', '1'), ('sa', 'sb', '1'), ('sb', 'sb', '1'),
                              ('sa', 'sa', '2'), ('sb', 'sb', '2')]


        self.assertItemsEqual(relations_as_tuples, expected_relations)

        sa = self.model.get_state_by_name('sa')
        sa_relations_as_tuple = relations_to_list_of_string_tuples(sa.outgoing['1'])
        sa_expected_relations = [('sa', 'sa','1'), ('sa', 'sb', '1')]
        self.assertItemsEqual(sa_relations_as_tuple, sa_expected_relations)

        sa_relations_as_tuple = relations_to_list_of_string_tuples(sa.outgoing['2'])
        sa_expected_relations = [('sa', 'sa', '2')]
        self.assertItemsEqual(sa_relations_as_tuple, sa_expected_relations)

        sa_relations_as_tuple = relations_to_list_of_string_tuples(sa.incoming['1'])
        sa_expected_relations = [('sa', 'sa', '1')]
        self.assertItemsEqual(sa_relations_as_tuple, sa_expected_relations)

        sa_relations_as_tuple = relations_to_list_of_string_tuples(sa.incoming['2'])
        sa_expected_relations = [('sa', 'sa', '2')]
        self.assertItemsEqual(sa_relations_as_tuple, sa_expected_relations)

class TestS4Model(TestCase):
    def setUp(self):
        filename = './modelchecker/models/test_model_s4.json'
        data = translators.read_json(filename)
        self.model = models.S4Model.from_json(data)

    def test_reflexive_closure(self):
        relations_as_tuples = [
            relations_to_list_of_string_tuples(relations)
            for (_, relations) in self.model.relations.iteritems()
        ]
        relations_as_tuples = flatten(relations_as_tuples)
        expected_relations = [('sa', 'sa', '1'), ('sb', 'sb', '1'), ('sc', 'sc', '1'), ('sd', 'sd', '1'),
                              ('sa', 'sb', '1'), ('sb', 'sc', '1'), ('sa', 'sc', '1'),
                              ('sa', 'sa', '2'), ('sb', 'sb', '2'), ('sc', 'sc', '2'), ('sd', 'sd', '2'),
                              ('sa', 'sb', '2'), ('sb', 'sc', '2'), ('sc', 'sd', '2'), ('sa', 'sc', '2'),
                              ('sa', 'sd', '2'), ('sb', 'sd', '2')
        ]


        self.assertItemsEqual(relations_as_tuples, expected_relations)

class TestS5Model(TestCase):
    def setUp(self):
        filename = './modelchecker/models/test_model_s5.json'
        data = translators.read_json(filename)
        self.model = models.S5Model.from_json(data)

    def test_reflexive_closure(self):
        relations_as_tuples = [
            relations_to_list_of_string_tuples(relations)
            for (_, relations) in self.model.relations.iteritems()
        ]
        relations_as_tuples = flatten(relations_as_tuples)
        expected_relations = [('sa', 'sa', '1'), ('sb', 'sb', '1'), ('sc', 'sc', '1'),
                              ('sa', 'sb', '1'), ('sb', 'sa', '1'),
                              ('sa', 'sa', '2'), ('sb', 'sb', '2'), ('sc', 'sc', '2'),
                              ('sb', 'sc', '2'), ('sc', 'sb', '2')
        ]
        self.assertItemsEqual(relations_as_tuples, expected_relations)