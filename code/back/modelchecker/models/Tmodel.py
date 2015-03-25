# -*- coding: utf-8 -*-

__author__ = 'laura'

from KMmodel import KMmodel
from relation import  Relation

class TModel(KMmodel):
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
        for agent in self.relations.keys():
            for _, state in self.states.iteritems():
                self.add_relation(
                    Relation(
                        agent,
                        state,
                        state
                    )
                )

    def add_relations_from_json(self, json_data):
        super(TModel, self).add_relations_from_json(json_data)
        self.reflexive_closure()
