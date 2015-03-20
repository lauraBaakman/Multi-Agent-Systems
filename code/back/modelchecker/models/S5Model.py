# -*- coding: utf-8 -*-

__author__ = 'laura'

import kmmodel

class S5KMModel(kmmodel.KMModel):
    """
        Class representing an S5KMModel
    """

    def __init__(self):
        super(S5KMModel, self).__init__()
        raise NotImplementedError

    def add_state(self, state):
        """
        Add a state to the list of states
        :param relation: the state to be added to the models
        :return:
        """
        raise NotImplementedError

    def add_relation(self, relation):
        """
        Add the relation to the list of relations of the models and add the relation to respectively the incoming and
        outgoing list its the destination and source node.
        :param relation: Relation
        :return: void
        """
        raise NotImplementedError