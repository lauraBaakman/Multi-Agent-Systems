# -*- coding: utf-8 -*-

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

    def set_truth_value(self, proposition, truth_value=True):
        """
        Set the truth value of a proposition.
        :param proposition: the proposition to set the truth value of.
        :param truth_value: [optional] the truth value to set, default is true.
        :return: void
        """
        try:
            self.valuations[proposition] = truth_value
        except KeyError:
            print "Unknown proposition encountered, did not set truth value."

    def __repr__(self):
        # TODO show incoming, outgoing states and valuation as well.
        return "{obj.name}".format(obj = self)

