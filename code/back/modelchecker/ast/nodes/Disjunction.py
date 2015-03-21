# -*- coding: utf-8 -*-

__author__ = 'laura'

from node import Node, models
from string import Template

class Disjunction(Node):

    def __init__(self, lhs=None, rhs=None):
        self.rhs = rhs
        self.lhs = lhs

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "({obj.lhs} OR {obj.rhs})".format(obj=self)
        )

    def is_true(self, state):
        """
        Determine the truth value of this formula.
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :return: (truthvalue, dict) truthvalue is the truth value of the formula, dict contains the motivation.
        :rtype: (bool, dict)
        """
        (lhs_truth_value, lhs_result) = self.lhs.is_true(state)
        (rhs_truth_value, rhs_result) = self.rhs.is_true(state)
        truth_value = lhs_truth_value or rhs_truth_value
        return (
            truth_value,
            {
                'condition': self._condition(state),
                'interlude': [lhs_result, rhs_result],
                'conclusion': self._conclusion(state, lhs_truth_value, rhs_truth_value, truth_value),
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
        return '{lhs_models} or {rhs_models}'.format(
            lhs_models=models(state, self.lhs, '$'),
            rhs_models=models(state, self.rhs, '$'),
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
        if (lhs_truth_value):
            return '{models} holds since {condition}.'.format(
                models=models(state, self, '$'),
                condition=models(state, self.lhs, '$')
            )
        elif rhs_truth_value:
            return '{models} holds since {condition}.'.format(
                models=models(state, self, '$'),
                condition=models(state, self.rhs, '$')
            )
        else:
            return '{models} does not hold since neither {condition_lhs} nor {condition_rhs} holds.'.format(
                models=models(state, self, '$'),
                condition_lhs=models(state, self.lhs, '$'),
                condition_rhs=models(state, self.rhs, '$')
            )

    def to_latex(self, delimiter=''):
        """
        Return LaTeX representation
        :param delimiter: [optional, default = ''] delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        return '{delimiter}\\left({lhs}\\lor{rhs}\\right){delimiter}'.format(
            delimiter=delimiter,
            lhs=self.lhs.to_latex(),
            rhs=self.rhs.to_latex()
        )