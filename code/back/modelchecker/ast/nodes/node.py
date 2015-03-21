# -*- coding: utf-8 -*-

__author__ = 'laura'

import abc

def models(state, formula, delimiter=''):
    return "{delimiter}\left(M, \\text{{{state}}} \\right) \models {formula}{delimiter}".format(
        state=state.name,
        formula=formula.to_latex(),
        delimiter=delimiter
    )

class Node(object):
    """General node class"""
    __metaclass__ = abc.ABCMeta

    def _condition(self, state):
        return '{models} iff {condition}.'.format(
            models=models(state, self, '$'),
            condition=self._truth_condition(state)
        )

    @abc.abstractmethod
    def _truth_condition(self):
        pass