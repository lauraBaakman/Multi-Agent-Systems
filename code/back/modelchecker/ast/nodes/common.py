# -*- coding: utf-8 -*-

__author__ = 'laura'

from unary import Unary
from node import models

class Common(Unary):
    def __init__(self, lhs=None):
        super(Common, self).__init__(lhs)

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "(COMMON {obj.lhs})".format(obj=self)
        )

    def is_true(self, state):
        """
        Determine the truth value of this formula.
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :return: (truthvalue, dict) truthvalue is the truth value of the formula, dict contains the motivation.
        :rtype: (bool, dict)
        """
        return  super(Common, self).is_true(
            state=state,
            destination_states=list(state.model.all_states_eventually_reachable_from(state) | {state})
        )

    def _truth_condition(self, state):
        """
        Return the condition under which this formula is true as a string.
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :return: String with the truth condition
        :rtype: String
        """
        return '{lhs_models} for all $t$ with ${state} \\twoheadrightarrow t$'.format(
            lhs_models=models('t', self.lhs, '$'),
            state=state.name
        )

    def to_latex(self, delimiter='', operator='\\text{{C}}'):
        """
        Return LaTeX representation
        :param: operator: operator
        :type operator: str
        :param delimiter: [optional, default = ''] delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        return super(Common, self).to_latex(operator=operator, delimiter=delimiter)