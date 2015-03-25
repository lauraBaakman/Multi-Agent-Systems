# -*- coding: utf-8 -*-

__author__ = 'laura'

from modelchecker.models import KMModel

class TModel(KMModel):
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
        raise NotImplementedError

    def add_relations_from_json(self, json_data):
        super(TModel, self).add_relations_from_json(json_data)
        self.reflexive_closure()
