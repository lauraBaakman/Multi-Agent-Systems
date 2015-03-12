"""."""
from enum import Enum
import re


import config
import tokens

class BinaryOperators(Enum):
    conjunction = 1
    disjunction  = 2
    implication = 3
    biimplication = 4

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


def _get_regular_expression(logic):
    """
    Create a list of regular expressions to tokenize the formula.
    :param logic: the logic to be used, options: KM, S5, S5EC
    :return: a list of regular expressions.
    """
    km_s5_expressions = [
        (config.kms5['knowledge'], lambda scanner, token: tokens.Knowledge(token)),
        (config.kms5['possible'],  lambda scanner, token: tokens.Possible(token))
    ]

    s5EC_expressions = [
        (config.common['common'], lambda scanner, _: tokens.Common())
    ]

    expressions_per_logic = {
        "KM":   km_s5_expressions,
        "S5":   km_s5_expressions,
        "S5EC": s5EC_expressions
    }

    expressions = [
        (r"[a-z]\w*",                              lambda scanner,  token: tokens.Proposition(token)),
        (config.propositional['conjunction'],      lambda scanner,      _: tokens.BinaryOperator(BinaryOperators.conjunction)),
        (config.propositional['disjunction'],      lambda scanner,      _: tokens.BinaryOperator(BinaryOperators.disjunction)),
        (config.propositional['implication'],      lambda scanner,      _: tokens.BinaryOperator(BinaryOperators.implication)),
        (config.propositional['bi-implication'],   lambda scanner,      _: tokens.BinaryOperator(BinaryOperators.biimplication)),
        (config.propositional['negation'],         lambda scanner,      _: tokens.Negation()),
        # TODO extend skip token to tabs and newlines
        (r"\s+", None), # None == skip token.
        # TODO add brackets
    ]

    expressions.extend(expressions_per_logic.get(logic, []))
    return expressions

def tokenize(logic, string):
    """
    Tokenize the inputted string to a list of tokens
    :param loigc: The logic of the string, options: KM, S5, S5EC
    :param string: The string to be converted to tokens.
    :return:[object]
    """
    regular_expressions = _get_regular_expression(logic);
    scan = re.Scanner(regular_expressions)
    results, remainder=scan.scan(input_formula)

    if remainder:
        msg = "Could not parse some part of the expression, you probably " \
              "used an operator that is not defined (for this logic)."
        raise TokenizeError(remainder, msg)
    return results

if __name__ == "__main__":
    input_formula = "C ~a | K_47 c & q"
    logic = "KM"
    tokens = tokenize(logic, input_formula)
    print tokens