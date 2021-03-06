# -*- coding: utf-8 -*-

__author__ = 'laura'

from unary import Unary
from node import models

class Implicit(Unary):
    def __init__(self, lhs=None):
        super(Implicit, self).__init__(lhs)

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "(INTENTION {obj.lhs})".format(obj=self)
        )

    def is_true(self, state):
        """
        Determine the truth value of this formula.
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :return: (truthvalue, dict) truthvalue is the truth value of the formula, dict contains the motivation.
        :rtype: (bool, dict)
        """

        agent_iterator = iter(state.model.agents)
        relations = set(
            state.get_all_outgoing_as_two_tuple(agent_iterator.next())
        )
        for agent in agent_iterator:
            relations = relations.intersection(state.get_all_outgoing_as_two_tuple(agent))
        destination_states = [destination for (_, destination) in relations]
        return super(Implicit, self).is_true(
            state=state,
            destination_states=destination_states
        )


    def _conclusion_no_relations(self, state):
        return super(Implicit, self)._conclusion_no_relations(
            evaluation_state=state,
            empty_set=self._agents_as_string(
                agents=list(state.model.agents),
                operator='\cap'
            )
        )

    def _truth_condition(self, state):
        """
        Return the condition under which this formula is true as a string.
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :return: String with the truth condition
        :rtype: String
        """
        return '{lhs_models} for all $t$ such that $({state}, t) \in {set}$'.format(
            lhs_models=models('t', self.lhs, '$'),
            state=state.name,
            set=self._agents_as_string(
                agents = list(state.model.agents),
                operator = '\cap'
            )
        )


    def _conclusion(self, state, truth_value):
        """
        Return the conclusion motivation the truth value of this formula
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :param truth_value: the truth value of this formula
        :type truth_value: bool
        :return: String with the motivation
        :rtype: String
        """
        raise NotImplementedError


    def to_latex(self, delimiter='', operator='\\text{{I}}'):
        """
        Return LaTeX representation
        :param: operator: operator
        :type operator: str
        :param delimiter: [optional, default = ''] delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        return super(Implicit, self).to_latex(operator=operator, delimiter=delimiter)