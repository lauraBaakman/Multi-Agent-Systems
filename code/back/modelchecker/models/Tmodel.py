# -*- coding: utf-8 -*-

__author__ = 'laura'

from Kmodel import KModel
from relation import  Relation
import modelchecker.utils.closures as closures

class TModel(KModel):
    """
    Class representing reflexive Kripke models.
    Attributes:
        - states: A dictionary of states, indexed by state name.
        - relations: A dictionary of agents, indexed by agent name.
    """

    def __init__(self):
        super(TModel, self).__init__()

    def reflexive_closure(self):
        """
        Compute the reflexive closure of the relations in the model
        """
        states_in_model = self.states.values()
        for agent, relations in self.relations.iteritems():
            relations_as_set = set([relation.to_tuple() for relation in relations])
            closure = closures.reflexive(relations_as_set, states_in_model)
            closure.difference_update(relations_as_set)
            [
                self.add_relation(
                    Relation.from_tuple((source, destination, agent))
                )
                for (source, destination) in closure
            ]

    def add_relations_from_json(self, json_data):
        super(TModel, self).add_relations_from_json(json_data)
        self.reflexive_closure()
