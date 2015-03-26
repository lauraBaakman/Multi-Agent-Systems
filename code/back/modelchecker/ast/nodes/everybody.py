# -*- coding: utf-8 -*-

__author__ = 'laura'

from node import models
from unary import Unary

class Everybody(Unary):
    def __init__(self, lhs=None):
        super(Everybody, self).__init__(lhs)

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "(EVERYBODY {obj.lhs})".format(obj=self)
        )

    def is_true(self, state):
        """
        Determine the truth value of this formula.
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :return: (truthvalue, dict) truthvalue is the truth value of the formula, dict contains the motivation.
        :rtype: (bool, dict)
        """
        states = list(set([state for _, states in state.outgoing.iteritems() for state in states]))
        if not states:
            return self._is_true_no_relations(state)
        elif len(states) == 1:
            # There is one outgoing relation
            raise NotImplementedError
        else:
            # There are multiple outgoing relations
            raise NotImplementedError


    def _is_true_no_relations(self, state):
        truth_value = True
        conclusion = self._conclusion_no_relations(state)
        return (
            truth_value,
            {
                'condition': self._condition(state),
                'conclusion': conclusion,
            }
        )

    def _conclusion_no_relations(self, state):
        def union_of_relations(state):
            agents = list(state.model.agents)
            result = 'R_{}'.format(agents[0])
            for i in range(1, len(agents)):
                result = format('{} \cup R_{}'.format(result, agents[i]))
            return result

        return (
            '{models} holds since $\left\{{ ({state}, t) | ({state}, t)'
            ' \in {union}\\right\}} = \emptyset$.'.format(
                models=models(state, self, '$'),
                state=state.name,
                union=union_of_relations(state)
            )
        )

    def _truth_condition(self, state):
        """
        Return the condition under which this formula is true as a string.
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :return: String with the truth condition
        :rtype: String
        """
        return '{lhs_models} for all $t$ with ${state} \longrightarrow t$'.format(
            lhs_models=models('t', self.lhs, '$'),
            state=state.name
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

    def to_latex(self, delimiter='', operator='\\text{E}'):
        """
        Return LaTeX representation
        :param: operator: operator
        :type operator: str
        :param delimiter: [optional, default = ''] delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        return super(Everybody, self).to_latex(operator=operator, delimiter=delimiter)