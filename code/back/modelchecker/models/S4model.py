# -*- coding: utf-8 -*-

__author__ = 'laura'

from Tmodel import TModel
import modelchecker.utils.closures as closures
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

    def compute_closure(self, closure_function):
        """
        Compute the closure defined by closure_function.
        :param closure_function: Function that computes a closure, it should accept a set of tuples as input and
        output a set of tuples.
        """
        for agent, relations in self.relations.iteritems():
            relations_as_set = set([relation.to_tuple() for relation in relations])
            relations_as_set = set([(source, destination) for (source, destination, _) in relations_as_set])
            closure = closure_function(relations_as_set)
            closure.difference_update(relations_as_set)
            [
                self.add_relation(
                    Relation.from_tuple((source, destination, agent))
                )
                for (source, destination) in closure
            ]

    def transitive_closure(self):
        """
        Compute the transitive closure of the relations in the mdoel.
        """
        self.compute_closure(closures.transitive)

    def add_relations_from_json(self, json_data):
        super(S4Model, self).add_relations_from_json(json_data)
        self.transitive_closure()
