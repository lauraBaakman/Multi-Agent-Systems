# -*- coding: utf-8 -*-

__author__ = 'laura'

from node import Node, models

class Knowledge(Node):

    def __init__(self, agent, lhs=None):
        self.agent = agent
        self.lhs = lhs

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
        # todo Implement
        raise NotImplementedError
        # return (
        #     truth_value,
        #     {
        #         'condition': self._condition(state),
        #         'interlude': [lhs_result],
        #         'conclusion': self._conclusion(state, lhs_truth_value, rhs_truth_value, truth_value),
        #     }
        # )

    def _truth_condition(self, state):
        """
        Return the condition under which this formula is true as a string.
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :return: String with the truth condition
        :rtype: String
        """
        raise NotImplementedError

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

    def to_latex(self, delimiter=''):
        """
        Return LaTeX representation
        :param delimiter: [optional, default = ''] delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        return '{delimiter} \\text{{K}}_{{\\text{{{agent}}}}}\\left({lhs}\\right){delimiter}'.format(
            delimiter=delimiter,
            lhs=self.lhs.to_latex(),
            agent=self.agent
        )