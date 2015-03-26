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

    def transitive_closure(self):
        raise NotImplementedError

    def add_relations_from_json(self, json_data):
        super(S4Model, self).add_relations_from_json(json_data)
        self.transitive_closure()
