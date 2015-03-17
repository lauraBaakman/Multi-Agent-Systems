# -*- coding: utf-8 -*-

import state

__author__ = 'laura'


class ModelError(Exception):
    """ Exception raised for errors in the model."""
    pass


class Model(object):
    """
    Attributes:
        - states: A dictionary of states, indexed by state name.
        - relations: A dictionary of agents, indexed by agent name.
    """

    def __init__(self, states):
        """
        Constructor for Model
        :param states: dictonary of states indexed by their name.
        :return:
        """
        if (not states):
            raise ModelError("A model needs a non empty set of states.")
        self.states = states
        self.relations = {}

    def __repr__(self):
        """Print friendly representation"""
        return "States:\n {obj.states}\nRelations: {obj.relations}".format(obj=self)

    @staticmethod
    def from_json(json_data):
        """
        Generate a model from json_data
        :param json_data: json data
        :return: a model
        """

        # {
        # 'states': ['a', 'b', 'c', 'd'],
        #   'propositions': ['p', 'q'],
        #   'relations': [['a', 1, 'b'], ['c', 2, 'd']],
        #   'valuations': [['a', ['p', 'q']], ['d', ['q']]],
        #   'logic': 'K(m)'
        # }

        # TODO: Select correct model constructor given the logic.

        try:
            propositions = json_data['propositions']
            states = {state_name: state.State(state_name, propositions) for state_name in json_data['states']}
            [states[state_name].set_true(propositions) for [state_name, propositions] in json_data['valuations']]
        except ModelError:
            raise

        return Model(states)

        # Add relationshipsq

        # Add valuations to states
