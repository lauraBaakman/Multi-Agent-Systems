# -*- coding: utf-8 -*-

__author__ = 'laura'

from Tmodel import TModel
from relation import Relation

class S4Model(TModel):
    """
    Class representing reflexive Kripke models.
    Attributes:
        - states: A dictionary of states, indexed by state name.
        - relations: A dictionary of agents, indexed by agent name.
    """

    def __init__(self):
        super(S4Model, self).__init__()

    def _transitive_closure_of_a_set(self, relations):
        original_set = set([relation.to_tuple() for relation in relations])
        closure = original_set
        while True:
            new_relations = set((x, w, agent) for x, y, agent in closure for q, w, agent in closure if q == y)
            closure_until_now = closure | new_relations
            if closure_until_now == closure:
                break
            closure = closure_until_now
        new_relations = list(closure - original_set)
        [self.add_relation(Relation.from_tuple(relation)) for relation in new_relations]

    def transitive_closure(self):
        for agent, relations in self.relations.iteritems():
            self._transitive_closure_of_a_set(relations)

    def add_relations_from_json(self, json_data):
        super(S4Model, self).add_relations_from_json(json_data)
        self.transitive_closure()
