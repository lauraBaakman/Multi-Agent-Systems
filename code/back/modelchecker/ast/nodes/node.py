# -*- coding: utf-8 -*-

__author__ = 'laura'

from modelchecker.models.state import  State

def models(state, formula, delimiter=''):
    if isinstance(state, State):
        state = state.name
    return "{delimiter}\left(M, \\text{{{state}}} \\right) \models {formula}{delimiter}".format(
        state=state,
        formula=formula.to_latex(),
        delimiter=delimiter
    )

class Node(object):
    """General node class"""

    def _condition(self, state):
        return '{models} iff {condition}.'.format(
            models=models(state, self, '$'),
            condition=self._truth_condition(state)
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__