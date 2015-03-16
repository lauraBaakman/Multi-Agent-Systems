# -*- coding: utf-8 -*-

"""The parser handles the actual parsing of expressions."""

import tokenize.operators as operators
import tokenize.tokens as tokens
import nodes
import utils

__author__ = 'laura'


# TODO bouwen volgens http://www.engr.mun.ca/~theo/Misc/exp_parsing.htm#classic

class ParserError(IOError):
    """
    Exception raised when the string cannot be parsed
    """

    def __init__(self, msg):
        """
        Constructor for TokenizeError
        :param msg: explanation of the error
        """
        self.msg = msg


class Parser(object):
    """Parser object"""

    def __init__(self, precedence=None):
        """
        Constructor for parser object
        :param precedence: Dictionary with the different operators and their precedence. If it is not supplied a
        default is used.
        :return: AST
        """
        default_precedence = {
            operators.Unary.common: 7,
            operators.Agent.knowledge: 7,
            operators.Agent.possible: 7,

            operators.Unary.negation: 6,

            operators.Binary.conjunction: 5,

            operators.Binary.disjunction: 4,

            operators.Binary.implication: 3,

            operators.Binary.biimplication: 2,

            None: 1
        }
        if not precedence:
            precedence = default_precedence

        self.precedence = precedence
        self.tokens = []
        self.operators = utils.Stack()
        self.operands = utils.Stack()

    def parse(self, tokens):
        """
        Parse the list of tokens and create an AST
        :param tokens: as list of tokens
        :return: an AST
        """
        self.tokens = tokens
        self.operators.push(None)
        self.E()
        self.expect(None)
        return self.operands.top()

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
        if self.next() == expected_token:
            self.consume()
        else:
            raise ParserError(
                "Expected {expected} but found {found}.".format(
                    expected=expected_token,
                    found=self.next()
                )
            )

    def E(self):
        self.P()
        while isinstance(self.next(), tokens.BinaryOperator):
            node = nodes.Binary(self.next())
            self.pushOperator(node)
            self.consume()
            self.P()

        while self.operators.top():
            self.popOperator()

    def P(self):
        if isinstance(self.next(), tokens.Proposition):
            self.operands.push(nodes.Proposition(self.next()))
            self.consume()
        elif isinstance(self.next(), tokens.BracketOpen):
            self.consume()
            self.operators.push(None)
            self.E()
            self.expect(tokens.BracketClose)
            self.operators.pop()
        elif isinstance(self.next(), tokens.UnaryOperator):
            self.pushOperator(nodes.Unary(self.next()))
            self.consume()
            self.P()
        else:
            raise ParserError("Could not continue parsing")

    def popOperator(self):
        if isinstance(self.operators.top(), tokens.BinaryOperator):
            t1 = self.operands.pop()
            t2 = self.operands.pop()
            self.operands.push(
                self.makeNode(
                    self.operators.pop(),
                    t1,
                    t2
                )
            )
        elif isinstance(self.operators.top(), tokens.UnaryOperator):
            t1 = self.operands.pop()
            self.operands.push(
                self.makeNode(
                    self.operators.pop(),
                    t1
                )
            )
        elif isinstance(self.operators.top(), tokens.AgentOperator):
            t1 = self.pop(self.operands)
            self.operands.push(
                self.makeNode(
                    self.operators.pop(),
                    t1
                )
            )

    def pushOperator(self, operator):
        while self.precedence_is_higher(self.operators.top(), operator):
            self.popOperator()
        self.operators.push(operator)

    def precedence_is_higher(self, operator_1, operator_2):
        """
        Return true if the precedence of operator_1 is greater than that of operator_2.
        :param operator_1: operator
        :param operator_2: operator
        :return: boolean
        """
        print "Precedence functie"
        if (
                    isinstance(operator_1, tokens.BinaryOperator) and
                    isinstance(operator_2, tokens.BinaryOperator)
        ):
            return self.precedence.get(operator_1.type) > self.precedence.get(operator_2.type)

        if (
                    isinstance(operator_1, tokens.BinaryOperator) and
                    isinstance(operator_2, tokens.UnaryOperator)
        ):
            return self.precedence.get(operator_1.type) >= self.precedence.get(operator_2.type)

        if (
                    isinstance(operator_1, (tokens.BinaryOperator, tokens.UnaryOperator, tokens.AgentOperator)) and
                    isinstance(operator_2, tokens.UnaryOperator)
        ):
            return False
        if (operator_1 == None):
            return False
        else:
            raise ParserError("Error!")



    def makeNode(self, operator, lhs, rhs=None):
        """
        Create an actual node
        :return: Node
        """
        if (rhs):
            operator.lhs = lhs
            operator.rhs = rhs
        else:
            operator.lhs = lhs

        return operator

