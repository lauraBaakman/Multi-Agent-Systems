# -*- coding: utf-8 -*-

__author__ = 'laura'

from node import Node, models
from agent import Agent
from negation import  Negation
from knowledge import Knowledge

class Possible(Agent):

    def __init__(self, agent, lhs=None):
        super(Possible, self).__init__(agent, lhs)

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "(M_{obj.agent} {obj.lhs})".format(obj=self)
        )

    def rewrite(self):
        return Negation(
            lhs=Knowledge(
                agent=self.agent,
                lhs=Negation(
                    lhs=self.lhs
                )
            )
        )


    def is_true(self, state):
        """
        Determine the truth value of this formula.
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :return: (truthvalue, dict) truthvalue is the truth value of the formula, dict contains the motivation.
        :rtype: (bool, dict)
        """
        (truth_value, dict) = self.rewrite().is_true(state)
        dict['condition'] = '{rewrite} {rewrite_condition}'.format(
            rewrite=self._condition(state),
            rewrite_condition=dict['condition']
        )
        return (truth_value, dict)

    def _truth_condition(self, state):
        """
        Return the condition under which this formula is true as a string.
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :return: String with the truth condition
        :rtype: String
        """
        return '{models}'.format(
            models=models(state, self.rewrite(), '$'),
        )

    def _conclusion(self, state, lhs_truth_value, rhs_truth_value, truth_value):
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

    def to_latex(self, delimiter='', operator='\\text{M}'):
        """
        Return LaTeX representation
        :param: operator: operator
        :type operator: str
        :param delimiter: [optional, default = ''] delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        return super(Possible, self).to_latex(delimiter, operator)