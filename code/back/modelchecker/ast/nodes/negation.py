# -*- coding: utf-8 -*-

__author__ = 'laura'

from node import models
from unary import Unary

class Negation(Unary):
    def __init__(self, lhs=None):
        super(Negation, self).__init__(lhs)

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "(NOT {obj.lhs})".format(obj=self)
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
        truth_value = not lhs_truth_value
        return (
            truth_value,
            {
                'condition': self._condition(state),
                'interlude': [lhs_result],
                'conclusion': self._conclusion(state, truth_value),
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
        return 'not {lhs_models}'.format(
            lhs_models=models(state, self.lhs, '$'),
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
        if (truth_value):
            return '{models} holds since {condition} does not hold.'.format(
                models=models(state, self, '$'),
                condition=models(state, self.lhs, '$')
            )
        else:
            return '{models} does not hold since {condition} holds.'.format(
                models=models(state, self, '$'),
                condition=models(state, self.lhs, '$')
            )

    def to_latex(self, delimiter='', operator='\lnot'):
        """
        Return LaTeX representation
        :param: operator: operator
        :type operator: str
        :param delimiter: [optional, default = ''] delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        if(self.lhs.is_leaf()):
            return super(Negation, self).to_latex(delimiter, operator)
        else:
            return '{delimiter} {operator} {lhs}{delimiter}'.format(
                delimiter=delimiter,
                lhs=self.lhs.to_latex(),
                operator=operator
            )