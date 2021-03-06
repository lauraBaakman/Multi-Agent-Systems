# -*- coding: utf-8 -*-

__author__ = 'laura'

from node import models
from modelchecker.ast.nodes.agent import Agent


class Knowledge(Agent):
    def __init__(self, agent, lhs=None):
        super(Knowledge, self).__init__(agent, lhs)

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "(K_{obj.agent} {obj.lhs})".format(obj=self)
        )

    def is_true(self, state):
        """
        Determine the truth value of this formula.
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :return: (truthvalue, dict) truthvalue is the truth value of the formula, dict contains the motivation.
        :rtype: (bool, dict)
        """
        destination_states = [relation.destination for relation in state.outgoing.get(self.agent, [])]
        if not destination_states:
            return self._is_true_no_relation(
                evaluation_state=state
            )
        elif len(destination_states) == 1:
            return self._is_true_one_relation(
                evaluation_state=state,
                destination_state=destination_states[0]
            )
        else:
            return self._is_true_multiple_relations(
                evaluation_state=state,
                destination_states=destination_states
            )

    def _truth_condition(self, state, states=None):
        """
        Return the condition under which this formula is true as a string.
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :return: String with the truth condition
        :rtype: String
        """
        return '{lhs_models} for all $t$ with $({state}, t) \\in R_{{{agent}}}$'.format(
            lhs_models=models('t', self.lhs, '$'),
            agent=self.agent,
            state=state.name
        )

    def _conclusion_no_relations(self, state):
        """
        Return the conclusion motivation the truth value of this formula
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :param truth_value: the truth value of this formula
        :type truth_value: bool
        :return: String with the motivation
        :rtype: String
        """
        return super(Knowledge, self)._conclusion_no_relations(
            evaluation_state=state,
            empty_set='\\text{{R}}_{{{agent}}}'.format(agent=self.agent)
        )

    def to_latex(self, delimiter='', operator='\\text{K}'):
        """
        Return LaTeX representation
        :param: operator: operator
        :type operator: str
        :param delimiter: [optional, default = ''] delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        return super(Knowledge, self).to_latex(delimiter, operator)