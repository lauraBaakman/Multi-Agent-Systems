# -*- coding: utf-8 -*-

__author__ = 'laura'

from S4model import S4Model

class S5Model(S4Model):
    """
    Class representing reflexive Kripke models.
    Attributes:
        - states: A dictionary of states, indexed by state name.
        - relations: A dictionary of agents, indexed by agent name.
    """

    def __init__(self):
        super(S5Model, self).__init__()

    def symmetric_transitive_closure(self):
        """
        Compute the reflexive closure of the relations in the model
        """
        # TODO impement and test!
        raise NotImplementedError

    def add_relations_from_json(self, json_data):
        super(S4Model, self).add_relations_from_json(json_data)
        self.symmetric_transitive_closure()