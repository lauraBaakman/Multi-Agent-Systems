# -*- coding: utf-8 -*-

"""
Classes that define the nodes of the AST
"""

__author__ = 'laura'

from modelchecker import operators


class Node(object):
    """General node class"""

class Unary(Node):

    def __init__(self, type, lhs=None):
        """
        Constructor for unary nodes
        :param token: unary token
        :return: Unary Node
        """
        self.type = type
        self.lhs = lhs

    @classmethod
    def fromToken(cls, token):
        return cls(token.type)

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
            operators.Unary.negation: negation,
            operators.Unary.common: common,
            operators.Unary.everybody: everybody
        }
        return operator_to_function.get(self.type)(self.lhs, state)


class Agent(Unary):

    def __init__(self, type, agent, lhs=None):
        """
        Constructor for Agent nodes
        :param token: unary token
        :return:
        """
        super(Agent, self).__init__(type, lhs)
        self.agent = agent

    @classmethod
    def fromToken(cls, token):
        return cls(token.type, token.agent)

    def __repr__(self):
        """Print-friendly infix representation."""
        return (
            "({obj.type}_{obj.agent} {obj.lhs})".format(obj=self)
        )

    def is_true(self, state):
        # TODO geeft true terug als er geen relaties zijn voor deze agent uit die staat, is dat correct?
        def knowledge(lhs, state, agent):
            truth_value = True
            for outgoing_relation in state.outgoing.get(agent, []):
                truth_value = lhs.is_true(outgoing_relation.destination)
                if not truth_value:
                    break
            return truth_value

        def possible(lhs, state, agent):
            return (
                Unary(
                    type=operators.Unary.negation,
                    lhs=Agent(
                        type=operators.Agent.knowledge,
                        agent=agent,
                        lhs=Unary(
                            type=operators.Unary.negation,
                            lhs=lhs
                        )
                    )
                ).is_true(state)
            )

        operator_to_function = {
            operators.Agent.knowledge: knowledge,
            operators.Agent.possible: possible
        }
        return operator_to_function.get(self.type)(self.lhs, state, self.agent)


class Binary(Node):

    def __init__(self, type, lhs=None, rhs=None):
        """
        Constructor for binary nodes
        :param token: binary token
        :return: Binary Node
        """
        self.type = type
        self.rhs = rhs
        self.lhs = lhs

    @classmethod
    def fromToken(cls, token):
        return cls(token.type)

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
            return state.is_true(self.name)
        except:
            raise

