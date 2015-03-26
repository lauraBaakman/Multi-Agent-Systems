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
            return self._is_true_no_relations(state)
        elif len(states) == 1:
            return self._is_true_one_relation(
                evaluation_state=state,
                destination_state=states[0]
            )
        else:
            return self._is_true_multiple_relations(state=state, destination_states=states)

    def _is_true_no_relations(self, state):
        return (
            True,
            {
                'condition': self._condition(state),
                'conclusion': self._conclusion_no_relations(state)
            }
        )

    def _is_true_multiple_relations(self, state, destination_states):
        interlude = []
        for destination in destination_states:
            (destination_truth_value, destination_motivation) = self.lhs.is_true(destination)
            if destination_truth_value:
                interlude.append(destination_motivation)
                truth_value = destination_truth_value
            else:
                truth_value = destination_truth_value
                interlude = [destination_motivation]
                conclusion = self._conclusion_one_relation(state, truth_value, destination)
                break
        if truth_value:
            conclusion = self._conclusion_multiple_relations(state, destination_states)

        return (
            truth_value,
            {
                'condition': self._condition(state),
                'interlude': interlude,
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

    def _conclusion_one_relation(self, state, truth_value, reached_state):
        if (truth_value):
            return '{models} holds since {condition} holds.'.format(
                models=models(state, self, '$'),
                condition=models(reached_state, self.lhs, '$')
            )
        else:
            return '{models} does not hold since {condition} does not hold.'.format(
                models=models(state, self, '$'),
                condition=models(reached_state, self.lhs, '$')
            )

    def _conclusion_multiple_relations(self, state, destination_states):
        conclusion = '{models} holds since '.format(
            models=models(state, self, '$'),
        )
        for state_idx in range(len(destination_states) - 1):
            destination_state = destination_states[state_idx].name
            conclusion = '{old_conclusion} {models}, '.format(
                old_conclusion=conclusion,
                models=models(destination_state, self.lhs, '$'),
            )
        return '{old_conclusion} and {models}.'.format(
            old_conclusion=conclusion,
            models=models(destination_states.pop().name, self.lhs, '$'),
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