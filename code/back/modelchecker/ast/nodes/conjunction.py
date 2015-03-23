# -*- coding: utf-8 -*-

__author__ = 'laura'

from node import models
from binary import Binary
from string import Template

class Conjunction(Binary):

    def __init__(self, lhs=None, rhs=None):
        super(Conjunction, self).__init__(lhs, rhs)

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "({obj.lhs} AND {obj.rhs})".format(obj=self)
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
        truth_value = lhs_truth_value and rhs_truth_value
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
        return '{lhs_models} and {rhs_models}'.format(
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
        if (truth_value):
            return '{models} holds since {condition}.'.format(
                models=models(state, self, '$'),
                condition=self._truth_condition(state)
            )
        else:
            conclusion = Template('$models does not hold since $reason.')

            if lhs_truth_value:
                reason = '{condition} does not hold'.format(condition=models(state, self.rhs, '$'))
            elif rhs_truth_value:
                reason = '{condition} does not hold'.format(condition=models(state, self.lhs, '$'))
            else:
                reason = '{condition_lhs} and {condition_rhs} do not hold'.format(
                    condition_lhs=models(state, self.lhs, '$'),
                    condition_rhs=models(state, self.rhs, '$')
                )
            return conclusion.substitute(reason=reason, models=models(state, self, '$'))

    def to_latex(self, delimiter='', operator='\land'):
        """
        Return LaTeX representation
        :param: operator: operator
        :type operator: str
        :param delimiter: [optional, default = ''] delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        return super(Conjunction, self).to_latex(delimiter, operator)