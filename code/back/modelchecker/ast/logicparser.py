# -*- coding: utf-8 -*-

"""
The parser handles the actual parsing of expressions.

 Grammar:

 E -> T '&' T | T '|' T | T '->' T | T '<->' T
 T -> C F | K F | M F
 F -> prop | '(' E ')' | '~' E

"""

from modelchecker import operators
from modelchecker.errors import ParserError
import modelchecker.tokenize.tokens as tokens
from modelchecker.ast.nodes import nodeFactory

__author__ = 'laura'


# Inspired by http://www.engr.mun.ca/~theo/Misc/exp_parsing.htm#classic


class END(object):

    def __repr__(self):
        return "END"

class Parser(object):
    """Parser object"""

    def __init__(self):
        """
        Constructor for parser object
        :return: AST
        """
        self.tokens = []

    def next(self):
        """
        Return the next token of the input, or None, if there are no more input tokens. Next() does not alter the
        input stream.
        :return: the next token or None if there are no more tokens.
        """
        if not self.tokens:
            return None
        else:
            return self.tokens[0]

    def consume(self):
        """
        Reads one token, is still allowed when self.next = None but has no effect in that case.
        :return: void
        """
        if self.next():
            self.tokens.pop(0)

    def expect(self, expected_token):
        """
        Consume the next token if it is the expected_token, otherwise throw an error.
        :param expected_token: the expected token.
        :return: nothing
        :raises: ParserError if the expected token is not found.
        """
        if isinstance(self.next(), expected_token):
            self.consume()
        else:
            raise ParserError(
                "Expected {expected} but found {found}.".format(
                    expected=expected_token,
                    found=self.next()
                )
            )

    def f(self):
        if isinstance(self.next(), tokens.Proposition):
            t = nodeFactory.from_token(self.next())
            self.consume()
            return t
        elif isinstance(self.next(), tokens.BracketOpen):
            self.consume()
            t = self.e()
            self.expect(tokens.BracketClose)
            return t
        elif self.next().type == operators.Unary.negation:
            node = nodeFactory.from_token(self.next())
            node.lhs = self.e()
        else:
            raise ParserError("Could not parse the expression.")

    def t(self):
        if isinstance(self.next(), (tokens.BracketOpen, tokens.Proposition)):
            return self.f()
        elif isinstance(self.next(), tokens.AgentOperator):
            node = nodeFactory.from_token(self.next())
        else:
            node = nodeFactory.from_token(self.next())
        # Execute this for both agent and unary tokens
        self.consume()
        node.lhs = self.e()
        return node

    def e(self):
        t = self.t()
        while isinstance(self.next(), tokens.BinaryOperator):
            node = nodeFactory.from_token(self.next())
            self.consume()
            t1 = self.t()
            node.rhs = t1
            node.lhs = t
            t = node
        return t

    def parse(self, tokens):
        """
        Parse the list of tokens and create an AST
        :param tokens: as list of tokens
        :return: an AST
        """
        self.tokens = tokens
        self.tokens.append(END())
        t = self.e()
        self.expect(END)
        return t







