# -*- coding: utf-8 -*-

__author__ = 'laura'

from unary import Unary
from node import models

class Intention(Unary):
    def __init__(self, lhs=None):
        super(Intention, self).__init__(lhs)

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "(INTENTION {obj.lhs})".format(obj=self)
        )

    def is_true(self, state):
        """
        Determine the truth value of this formula.
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :return: (truthvalue, dict) truthvalue is the truth value of the formula, dict contains the motivation.
        :rtype: (bool, dict)
        """
        raise NotImplementedError


    def _truth_condition(self, state):
        """
        Return the condition under which this formula is true as a string.
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :return: String with the truth condition
        :rtype: String
        """
        # In Everybody._conclusion_no_relations.union_of_realtions a string representing the untion of all relations in computed. Reuse for the truth condition here.
        raise NotImplementedError


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
        raise NotImplementedError


    def to_latex(self, delimiter='', operator='\\text{{I}}'):
        """
        Return LaTeX representation
        :param: operator: operator
        :type operator: str
        :param delimiter: [optional, default = ''] delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        return super(Intention, self).to_latex(operator=operator, delimiter=delimiter)