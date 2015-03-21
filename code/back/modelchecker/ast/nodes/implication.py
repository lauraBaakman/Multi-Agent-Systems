# -*- coding: utf-8 -*-

__author__ = 'laura'

from node import Node, models
from disjunction import  Disjunction
from negation import  Negation

class Implication(Node):

    def __init__(self, lhs=None, rhs=None):
        self.rhs = rhs
        self.lhs = lhs

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "({obj.lhs} -> {obj.rhs})".format(obj=self)
        )

    def is_true(self, state):
        """
        Determine the truth value of this formula.
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :return: (truthvalue, dict) truthvalue is the truth value of the formula, dict contains the motivation.
        :rtype: (bool, dict)
        """
        (truth_value, dict) = (
            Disjunction(
                lhs=Negation(
                    self.lhs
                ),
                rhs=self.rhs
            )
        ).is_true(state)
        dict['interlude'].insert(0, self._condition(state))
        return (truth_value, dict)


    def _truth_condition(self, state):
        """
        Return the condition under which this formula is true as a string.
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :return: String with the truth condition
        :rtype: String
        """
        return 'not {lhs_models} or {rhs_models}'.format(
            lhs_models=models(state, self.lhs, '$'),
            rhs_models=models(state, self.rhs, '$'),
        )

    def to_latex(self, delimiter=''):
        """
        Return LaTeX representation
        :param delimiter: [optional, default = ''] delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        return '{delimiter}\\left({lhs}\\to{rhs}\\right){delimiter}'.format(
            delimiter=delimiter,
            lhs=self.lhs.to_latex(),
            rhs=self.rhs.to_latex()
        )