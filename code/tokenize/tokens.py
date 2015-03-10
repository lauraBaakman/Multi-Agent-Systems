# -*- coding: utf-8 -*-

"""
The definitions of the tokens
"""
import tokenizer

__author__ = 'laura'


class KnowsToken(object):
    """Token representing the knows operator (K)"""

    def __init__(self, agent):
        self.agent = agent

    def __repr__(self):
        """Print-friendly representation of the Knows object."""
        return (
            "K_{obj.agent}".format(obj=self)
        )

class PossibleToken(object):
    """Token representing the possible operator (M)"""

    def __init__(self, agent):
        self.agent = agent

    def __repr__(self):
        """Print-friendly representation of the Possible object."""
        return (
            "M_{obj.agent}".format(obj=self)
        )

class CommonKnowledgeToken(object):
    """Token representing the common knowledge (T)"""

    def __repr__(self):
        """Print-friendly representation of the CommonKnowledge_token object."""
        return ("C")

class TrueToken(object):
    """Token representing the truth (T)"""

    def __repr__(self):
        """Print-friendly representation of the True_token object."""
        return ("T")

class FalseToken(object):
    """Token representing the absurdum (F)"""

    def __repr__(self):
        """Print-friendly representation of the False_token object."""
        return ("F")

class BracketOpen(object):
    """Token representing the bracket open (()"""

    def __repr__(self):
        """Print-friendly representation of the False_token object."""
        return ("(")

class BracketClose(object):
    """Token representing the bracket close ())"""

    def __repr__(self):
        """Print-friendly representation of the False_token object."""
        return (")")

class BinaryOperator(object):
    """
    Token representing binary operators
    """
    def __init__(self, operator):
        mapping = {
            "|" : tokenizer.BinaryOperators.or_op,
            "&" : tokenizer.BinaryOperators.and_op,
            "->": tokenizer.BinaryOperators.implication_op,
            "<->":tokenizer.BinaryOperators.bi_implication_op
        }

        self.operator = mapping.get(operator)

    def __repr__(self):
        """Print-friendly representation of the Binary_Operator object."""
        return ("{obj.operator.value}".format(obj=self))

class NotOperator(object):
    """
    Token representing the not
    """
    def __repr__(self):
        """Print-friendly representation of the Not_operator object."""
        return ("!")

class PropositionToken(object):
    """
    Token representing a propostion
    """
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        """Print-friendly representation of the proposition  object."""
        return ("{obj.name}".format(obj=self))