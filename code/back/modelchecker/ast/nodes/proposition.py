# -*- coding: utf-8 -*-
from node import models
from modelchecker.ast.nodes.node import Node

__author__ = 'laura'


class Proposition(Node):

    def __init__(self, name):
        self.name = name

    @classmethod
    def fromToken(cls, token):
        return cls(token.name)

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "{obj.name}".format(obj=self)
        )

    def is_true(self, state):
        """
        Return true if this proposition is true in the passed state in the passed model.
        :param model: A model
        :param state: A state object
        :return: Boolean
        """
        try:
            truth_value = state.is_true(self.name)
            condition = self._condition(state)
            conclusion = self._conclusion(state, truth_value)
            return {
                       'truth value': truth_value,
                       'condition': condition,
                       'conclusion': conclusion
            }
        except:
            raise

    def _condition(self, state):
        return '{models} iff {condition}.'.format(
            models=models(state, self, '$'),
            condition=self._truth_condition(state, 1)
        )

    def _truth_condition(self, state, value):
        return '$\pi\left({state_name}\\right)\left( {prop_name} \\right) = {value}$'.format(
            state_name=state.name,
            prop_name=self.name,
            value=value
        )

    def _conclusion(self, state, truth_value):
        if truth_value:
            return '{models} holds since {condition}.'.format(
                models=models(state, self, '$'),
                condition=self._truth_condition(state, int(truth_value))
            )
        else:
            return '{models} does not hold since {condition}.'.format(
                models=models(state, self, '$'),
                condition=self._truth_condition(state, int(truth_value))
            )

    def to_latex(self, delimiter = ''):
        """
        Return LaTeX representation
        :param delimiter: [optional, default = ''] delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        return '{delimiter}\\text{{{name}}}{delimiter}'.format(delimiter=delimiter, name=self.name)