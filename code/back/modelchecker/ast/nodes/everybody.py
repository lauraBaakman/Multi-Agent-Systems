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
        states = list(set([s.destination for _, states in state.outgoing.iteritems() for s in states]))
        if not states:
            return self._is_true_no_relation(
                evaluation_state=state
            )
        elif len(states) == 1:
            return self._is_true_one_relation(
                evaluation_state=state,
                destination_state=states[0]
            )
        else:
            return self._is_true_multiple_relations(
                evaluation_state=state,
                destination_states=states
            )

    def _conclusion_no_relations(self, state):
        def union_of_relations(state):
            agents = list(state.model.agents)
            result = 'R_{}'.format(agents[0])
            for i in range(1, len(agents)):
                result = format('{} \cup R_{}'.format(result, agents[i]))
            return result

        return super(Everybody, self)._conclusion_no_relations(
            evaluation_state=state,
            empty_set=union_of_relations(state)
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