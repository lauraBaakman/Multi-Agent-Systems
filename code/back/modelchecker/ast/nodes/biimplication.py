# -*- coding: utf-8 -*-

__author__ = 'laura'

from node import Node, models
from conjunction import Conjunction
from implication import Implication
from binary import Binary

class BiImplication(Binary):

    def __init__(self, lhs=None, rhs=None):
        super(BiImplication, self).__init__(lhs, rhs)

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "({obj.lhs} <-> {obj.rhs})".format(obj=self)
        )

    def rewrite(self):
        return Conjunction(
            lhs=Implication(
                lhs=self.lhs,
                rhs=self.rhs
            ),
            rhs=Implication(
                lhs=self.rhs,
                rhs=self.lhs
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

    def to_latex(self, delimiter='', operator='\\leftrightarrow'):
        """
        Return LaTeX representation
        :param: operator: operator
        :type operator: str
        :param delimiter: [optional, default = ''] delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        return super(BiImplication, self).to_latex(delimiter, operator)