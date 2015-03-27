# -*- coding: utf-8 -*-
from modelchecker.ast.nodes.node import Node, models

__author__ = 'laura'

class Unary(Node):
    def __init__(self, lhs):
        self.lhs = lhs

    def to_latex(self, delimiter, operator):
        """
        Return LaTeX representation
        :param: operator: operator
        :type operator: str
        :param delimiter: delimiters for the LaTeX representation.
        :type delimiter: str
        :return: LaTeX representation
        :rtype: str
        """
        return '{delimiter} {operator} \left({lhs}\\right){delimiter}'.format(
            delimiter=delimiter,
            lhs=self.lhs.to_latex(),
            operator=operator
        )

    def is_leaf(self):
        return False


    def is_true(self, state, destination_states):
        """
        Determine the truth value of this formula.
        :param state: the state in which the formula should be evaluated.
        :type state: modelchecker.models.state
        :param destination_states: the list of states in which lhs should be evaluated.
        :type state: list(modelchecker.models.state)
        :return: (truthvalue, dict) truthvalue is the truth value of the formula, dict contains the motivation.
        :rtype: (bool, dict)
        """
        if not destination_states:
            return self._is_true_no_relation(
                evaluation_state=state
            )
        elif len(destination_states) == 1:
            return self._is_true_one_relation(
                evaluation_state=state,
                destination_state=destination_states[0]
            )
        else:
            return self._is_true_multiple_relations(
                evaluation_state=state,
                destination_states=destination_states
            )

    def _is_true_one_relation(self, evaluation_state, destination_state):
        """
        Determine the truth value if one state can be reached.
        :param evaluation_state: the state in which the formula should be evaluated.
        :type evaluation_state: modelchecker.models.state
        :param destination_state: the state that could be reached.
        :param destination_state: modelchecker.models.state.State
        """
        (truth_value, motivation) = self.lhs.is_true(destination_state)
        return (
            truth_value,
            {
                'condition': self._condition(evaluation_state),
                'interlude': [motivation],
                'conclusion': self._conclusion_one_relation(evaluation_state, truth_value, destination_state)
            }
        )

    def _is_true_no_relation(self, evaluation_state):
        """
        Determine the truth value if no states can be reached.
        :param evaluation_state: the state in which the formula should be evaluated.
        :type evaluation_state: modelchecker.models.state
        """
        return (
            True,
            {
                'condition': self._condition(evaluation_state),
                'conclusion': self._conclusion_no_relations(evaluation_state),
            }
        )

    def _is_true_multiple_relations(self, evaluation_state, destination_states):
        """
        Determine the truth value if multiple states can be reached.
        :param evaluation_state: the state in which the formula should be evaluated.
        :type evaluation_state: modelchecker.models.state
        :param destination_states: the states that could be reached.
        :type destination_states: list(modelchecker.models.state.State)
        """
        interlude = []
        for destination in destination_states:
            (destination_truth_value, destination_motivation) = self.lhs.is_true(destination)
            if destination_truth_value:
                interlude.append(destination_motivation)
                truth_value = destination_truth_value
            else:
                truth_value = destination_truth_value
                interlude = [destination_motivation]
                conclusion = self._conclusion_one_relation(evaluation_state, truth_value, destination)
                break
        if truth_value:
            conclusion = self._conclusion_multiple_relations(evaluation_state, destination_states)

        return (
            truth_value,
            {
                'condition': self._condition(evaluation_state),
                'interlude': interlude,
                'conclusion': conclusion,
            }
        )

    def _conclusion_one_relation(self, evaluation_state, truth_value, destination_state):
        """
        Return the conclusion motivation the truth value of this formula
        :param evaluation_state: the state in which the formula should be evaluated.
        :type evaluation_state: modelchecker.models.state
        :param truth_value: the truth value of this formula
        :type truth_value: bool
        :param destination_state: the state that could be reached.
        :param destination_state: modelchecker.models.state.State
        :return: String with the motivation
        :rtype: String
        """
        if (truth_value):
            return '{models} holds since {condition} holds.'.format(
                models=models(evaluation_state, self, '$'),
                condition=models(destination_state, self.lhs, '$')
            )
        else:
            return '{models} does not hold since {condition} does not hold.'.format(
                models=models(evaluation_state, self, '$'),
                condition=models(destination_state, self.lhs, '$')
            )

    def _conclusion_multiple_relations(self, evaluation_state, destination_states):
        """
        The conclusion generator when there are multiple relations.
        :param evaluation_state: The state in which the formula was evaluated.
        :type evaluation_state: modelchecker.models.state.State
        :param destination_states: The state which could be reached
        :type destination_states: list(modelchecker.models.state.State)
        :return: The conclusion string
        :rtype: basestring
        """
        conclusion = '{models} holds since '.format(
            models=models(evaluation_state, self, '$'),
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

    def _conclusion_no_relations(self, evaluation_state, empty_set):
        """
        The conclusion generator when there are no relations.
        :param evaluation_state: The state in which the formula was evaluated.
        :type evaluation_state: modelchecker.models.state.State
        :param empty_set: The set which was found to be empty, as string without curly braces.
        :type empty_set: basestring
        :return: The conclusion string
        :rtype: basestring
        """
        return (
            '{models} holds since $\left\{{ ({state}, t) | ({state}, t)'
            ' \in {empty_set}\\right\}} = \emptyset$.'.format(
                models=models(evaluation_state, self, '$'),
                state=evaluation_state.name,
                empty_set=empty_set
            )
        )

    def _agents_as_string(self, agents, operator):
        """
        Return the list of agents as a string seperated by a set operator.
        :param operator: The set operator as a string e.g. '\cap'
        :type operator: str
        :return: str
        :rtype: str
        """
        result = 'R_{}'.format(agents[0])
        for i in range(1, len(agents)):
            result = format('{result} {operator} R_{agent}'.format(
                result=result,
                operator=operator,
                agent=agents[i])
            )
        return result