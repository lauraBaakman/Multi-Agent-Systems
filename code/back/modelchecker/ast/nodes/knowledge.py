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
        relations = state.outgoing.get(self.agent)
        if not relations:
            truth_value = True
            conclusion = self._conclusion_no_relations(state)
        elif len(relations) == 1:
        # There is only one outgoing relation.
            raise NotImplementedError
        else:
        # There are multiple outgoing realtions.
            raise NotImplementedError


        return (
            truth_value,
            {
                'condition': self._condition(state),
                # 'interlude': [lhs_result],
                'conclusion': conclusion,
            }
        )

    def _truth_condition(self, state):
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
            state=state
        )

    def _conclusion(self, state):
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
        return (
            '{models} holds since $\\left\\{{ ({state}, t) | ({state}, t)'
            ' \\in R_{{{agent}}}\\right\\}} = \\emptyset$.'.format(
            models=models(state, self, '$'),
            state=state.name,
            agent = self.agent
            )
        )

    def to_latex(self, delimiter='', operator='\\text{{K}}'):
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