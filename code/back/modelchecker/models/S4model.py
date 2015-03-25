# -*- coding: utf-8 -*-

__author__ = 'laura'

from Tmodel import TModel

class S4Model(TModel):
    """
    Class representing reflexive Kripke models.
    Attributes:
        - states: A dictionary of states, indexed by state name.
        - relations: A dictionary of agents, indexed by agent name.
    """

    def __init__(self):
        super(S4Model, self).__init__()

    def transitive_closure(self):
        """
        Compute the reflexive closure of the relations in the model
        """
        raise NotImplementedError

    def add_relations_from_json(self, json_data):
        super(TModel, self).add_relations_from_json(json_data)
        self.transitive_closure()
