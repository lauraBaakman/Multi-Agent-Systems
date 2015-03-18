# -*- coding: utf-8 -*-

import model

__author__ = 'laura'


class State(object):
    """
    State object

    Attributes:
        - incoming: dictionary of incoming relations, indexed by agent.
        - outgoing: dictionary of outgoing relations, indexed by agent.
        - valuations: dictionary of valuations, indexed by proposition.
    """

    def __init__(self, name, propositions):
        """
        Constructor for State object
        :param propositions: list of strings representing the propositions in the model.
        :param name: name of the state
        """
        self.name = name
        self.incoming = {}
        self.outgoing = {}
        self.valuations = {proposition: False for proposition in propositions}

    def _add_relation(self, dictionary, relation):
        if relation.agent in dictionary:

    def add_outgoing_relation(self, relation):
        """
        Add outgoing relation to the state, do nothing if the relation already exists.
        :param relation: the relation
        :return: void
        """
        #TODO Implementeren
        raise NotImplementedError



    def add_incoming_relation(self, relation):
        """
        Add incoming relation to the state, do nothing if the relation already exists.
        :param relation: the relation
        :return: void
        """
        #TODO Implementeren
        raise NotImplementedError

    def set_true(self, propositions):
        """
        Set the truth value of each propositions in propositions to true.
        :param propositions: list of propositions.
        :return: void
        """
        try:
            [self._set_truth_value(proposition) for proposition in propositions]
        except model.ModelError:
            raise


    def _set_truth_value(self, proposition, truth_value=True):
        """
        Set the truth value of a proposition.
        :param proposition: the proposition to set the truth value of.
        :param truth_value: [optional] the truth value to set, default is true.
        :return: void
        """
        if proposition in self.valuations:
            self.valuations[proposition] = truth_value
        else:
            raise model.ModelError('Tried to set the truth value of a non-existent proposition.')

    def __repr__(self):
        # TODO show incoming, outgoing states and valuation as well.
        return "{obj.name} [in: [], out: [], valuations: {obj.valuations}]\n".format(obj = self)

