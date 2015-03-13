# coding=utf-8

"""."""
import re

import config
from tokenize.operators import Binary, Unary
import tokens


class TokenizeError(IOError):
    """
    Exception raised when the string cannot be tokenized.
    """

    def __init__(self, expr, msg):
        """
        Constructor for TokenizeError
        :param expr: input expression in which the error occurred
        :param msg: explanation of the error
        """
        self.expr = expr
        self.msg = msg


def _get_lexicon(logic):
    """
    Select the lexicon for the scanner based on the logic.
    :param logic: the logic to be used, options: KM, S5, S5EC
    :return: list[(regular_expression, lambda function)]
    """
    km_s5_expressions = [
        (config.kms5['knowledge'], lambda scanner, token: tokens.Knowledge(token)),
        (config.kms5['possible'],  lambda scanner, token: tokens.Possible(token))
    ]

    s5EC_expressions = [
        (config.common['common'], lambda scanner, _: tokens.UnaryOperator(Unary.common))
    ]

    expressions_per_logic = {
        "KM":   km_s5_expressions,
        "S5":   km_s5_expressions,
        "S5EC": s5EC_expressions
    }

    expressions = [
        (config.propositional['conjunction'],      lambda scanner,      _: tokens.BinaryOperator(Binary.conjunction)),
        (config.propositional['disjunction'],      lambda scanner,      _: tokens.BinaryOperator(Binary.disjunction)),
        (config.propositional['implication'],      lambda scanner,      _: tokens.BinaryOperator(Binary.implication)),
        (config.propositional['bi-implication'],   lambda scanner,      _: tokens.BinaryOperator(Binary.biimplication)),
        (config.propositional['negation'],         lambda scanner,      _: tokens.UnaryOperator(Unary.negation)),
        (r"[a-z]\w*",                              lambda scanner,  token: tokens.Proposition(token)),
        (r"[[{(<]",                                lambda scanner,      _: tokens.BracketOpen()),
        (r"[]})>]",                                lambda scanner,      _: tokens.BracketClose()),
        (r"\s+",                                   None), # None == skip token.
    ]

    expressions.extend(expressions_per_logic.get(logic, []))
    return expressions

def tokenize(logic, string):
    """
    Tokenize the inputted string to a list of tokens
    :param loigc: The logic of the string, options: KM, S5, S5EC
    :param string: The string to be converted to tokens.
    :raise TokenizeError: if a unknown character is in the string.
    :return:[object]
    """
    regular_expressions = _get_lexicon(logic);
    scan = re.Scanner(regular_expressions)
    results, remainder=scan.scan(input_formula)

    if remainder:
        msg = "Could not parse some part of the expression \"...{expression}\", you probably " \
              "used an operator that is not defined (for this logic).".format(expression = remainder)
        raise TokenizeError(remainder, msg)
    return results

if __name__ == "__main__":
    input_formula = "C ~ (a -> b)"
    logic = "S5EC"
    try:
        tokens = tokenize(logic, input_formula)
        print tokens
    except TokenizeError as e:
        print e.msg
