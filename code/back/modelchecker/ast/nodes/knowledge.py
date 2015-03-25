# -*- coding: utf-8 -*-

__author__ = 'laura'

from node import models
from modelchecker.ast.nodes.agent import Agent


class Knowledge(Agent):
    def __init__(self, agent, lhs=None):
        super(Knowledge, self).__init__(agent, lhs)

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "(K_{obj.agent} {obj.lhs})".format(obj=self)
        )

    def is_true(self, state):
        """
        Determine the truth value of this formula.
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :return: (truthvalue, dict) truthvalue is the truth value of the formula, dict contains the motivation.
        :rtype: (bool, dict)
        """
        relations = state.outgoing.get(self.agent)
        if not relations:
            # There is no outgoing relation.
            truth_value = True
            conclusion = self._conclusion_no_relations(state)
            return (
                truth_value,
                {
                    'condition': self._condition(state),
                    'conclusion': conclusion,
                }
            )
        elif len(relations) == 1:
            # There is only one outgoing relation.
            destination = relations[0].destination
            (truth_value, motivation) = self.lhs.is_true(destination)
            interlude = [motivation]
            conclusion =self. _conclusion_one_relation(state, truth_value, destination)
        else:
            # There are multiple outgoing relations.
            destination_states = []
            interlude = []
            for relation in relations:
                (destination_truth_value, destination_motivation) = self.lhs.is_true(relation.destination)
                if destination_truth_value:
                    destination_states.append(relation.destination.name)
                    interlude.append(destination_motivation)
                    truth_value = destination_truth_value
                else:
                    truth_value = destination_truth_value
                    interlude = [destination_motivation]
                    conclusion = self._conclusion_one_relation(state, truth_value, relation.destination)
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

    def _truth_condition(self, state, states=None):
        """
        Return the condition under which this formula is true as a string.
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :return: String with the truth condition
        :rtype: String
        """
        return '{lhs_models} for all $t$ with $({state}, t) \\in R_{{{agent}}}$'.format(
            lhs_models=models('t', self.lhs, '$'),
            agent=self.agent,
            state=state.name
        )

    def _conclusion_multiple_relations(self, state, destination_states_names):
        """
        Return the conclusion motivation the truth value of this formula
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :param truth_value: the truth value of this formula
        :type truth_value: bool
        :return: String with the motivation
        :rtype: String
        """
        conclusion = '{models} holds since '.format(
            models=models(state, self, '$'),
        )
        for state_idx in range(len(destination_states_names) - 1):
            destination_state = destination_states_names[state_idx]
            conclusion = '{old_conclusion} {models}, '.format(
                old_conclusion=conclusion,
                models=models(destination_state, self.lhs, '$'),
            )
        return '{old_conclusion} and {models}.'.format(
            old_conclusion=conclusion,
            models=models(destination_states_names.pop(), self.lhs, '$'),
        )

    def _conclusion_one_relation(self, state, truth_value, destination_state):
        """
        Return the conclusion motivation the truth value of this formula
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :param truth_value: the truth value of this formula
        :type truth_value: bool
        :return: String with the motivation
        :rtype: String
        """
        if(truth_value):
            return '{models} holds since {condition} holds.'.format(
                models=models(state, self, '$'),
                condition=models(destination_state, self.lhs, '$')
            )
        else:
            return '{models} does not hold since {condition} does not hold.'.format(
                models=models(state, self, '$'),
                condition=models(destination_state, self.lhs, '$')
            )

    def _conclusion_no_relations(self, state):
        """
        Return the conclusion motivation the truth value of this formula
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :param truth_value: the truth value of this formula
        :type truth_value: bool
        :return: String with the motivation
        :rtype: String
        """
        return (
            '{models} holds since $\left\{{ ({state}, t) | ({state}, t)'
            ' \in R_{{{agent}}}\\right\}} = \emptyset$.'.format(
            models=models(state, self, '$'),
            state=state.name,
            agent = self.agent
            )
        )

    def to_latex(self, delimiter='', operator='\text{K}'):
        """
        Return LaTeX representation
        :param: operator: operator
        :type operator: str
        :param delimiter: [optional, default = ''] delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        return super(Knowledge, self).to_latex(delimiter, operator)