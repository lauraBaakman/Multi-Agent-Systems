# -*- coding: utf-8 -*-
from unittest import TestCase

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
        self.model = models.KMModel.from_json(data)

    def test_states(self):
        self.assertItemsEqual(
            self.model.states.keys(),
            ['sa', 'sb', 'sc', 'sd'],
            'Test if all states from the model are in the list of states.'
        )

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


