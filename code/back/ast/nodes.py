# -*- coding: utf-8 -*-

"""
Classes that define the nodes of the AST
"""

__author__ = 'laura'

from tokenize import operators, tokens

class Node(object):
    """General node class"""

class Unary(Node):

    def __init__(self, token, lhs=None):
        """
        Constructor for unary nodes
        :param token: unary token
        :return: Unary Node
        """
        self.type = token.type
        self.lhs = lhs

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "({obj.type} {obj.lhs})".format(obj=self)
        )

    def is_true(self, state):
        def negation(lhs, state):
            return not lhs.is_true(state)

        def common(lhs, state):
            # TODO implement
            raise NotImplementedError

        def everybody(lhs, state):
            #TODO implement
            raise NotImplementedError

        operator_to_function = {
            operators.Unary.negation: negation(),
            operators.Unary.common: common(),
            operators.Unary.everybody: everybody()
        }
        return operator_to_function.get(self.type)(self.lhs, state)


class Agent(Unary):

    def __init__(self, token):
        """
        Constructor for Agent nodes
        :param token: unary token
        :return:
        """
        super(Unary, self).__init__(token)
        self.agent = token.agent

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "({obj.type}_{obj.agent} {obj.lhs})".format(obj=self)
        )

    def is_true(self, state):
        # TODO geeft true terug als er geen relaties zijn voor deze agent uit die staat, is dat correct?
        def knowledge(lhs, state, agent):
            truth_value = True
            for state in state.outgoing.get(agent, []):
                truth_value = lhs.is_true(state)
                if not truth_value:
                    break
            return truth_value

        def possible(lhs, state, agent):
            lhs_with_negation = Unary(

            )



        operator_to_function = {
            operators.Agent.knowledge: knowledge(),
            operators.Agent.possible: possible(),
        }
        return operator_to_function.get(self.type)(self.lhs, state, agent)


class Binary(Node):

    def __init__(self, token):
        """
        Constructor for binary nodes
        :param token: binary token
        :return: Binary Node
        """
        self.type = token.type
        self.rhs = None
        self.lhs = None

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "({obj.lhs} {obj.type} {obj.rhs})".format(obj=self)
        )

    def is_true(self, state):
        def conjunction(lhs, rhs,  state):
            return lhs.is_true(state) and rhs.is_true(state)

        def disjunction(lhs, rhs, state):
            return lhs.is_true(state) or rhs.is_true(state)

        def implication(lhs, rhs, state):
            return (not lhs.is_true(state)) or rhs.is_true(state)

        def biimplication(lsh, rhs, state):
            return implication(lsh, rhs, state) and implication(rhs, lsh, state)

        operator_to_function = {
            operators.Binary.conjunction: conjunction,
            operators.Binary.disjunction: disjunction,
            operators.Binary.implication: implication,
            operators.Binary.biimplication: biimplication
        }
        return operator_to_function.get(self.type)(self.lhs, self.rhs, state)


class Proposition(Node):

    def __init__(self, token):
        self.name = token.name

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
            return state.is_true(self.name)
        except:
            raise

