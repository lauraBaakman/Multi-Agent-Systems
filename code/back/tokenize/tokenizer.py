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


def _get_regular_expression(logic):
    """
    Create a list of regular expressions to tokenize the formula.
    :param logic: the logic to be used, options: KM, S5, S5EC
    :return: a list of regular expressions.
    """
    # TODO add stuff for KM/S5
    km_s5_expressions = []

    # TODO add stuff for S5EC
    s5EC_expressions = []

    expressions_per_logic = {
        "KM": km_s5_expressions,
        "S5": km_s5_expressions,
        "S5EC": s5EC_expressions
    }

    expressions = [
        (r"[a-z]\w*",                              lambda scanner,  token: tokens.Proposition(token)),
        (config.propositional['conjunction'],      lambda scanner,      _: tokens.BinaryOperator(BinaryOperators.conjunction)),
        (config.propositional['disjunction'],      lambda scanner,      _: tokens.BinaryOperator(BinaryOperators.disjunction)),
        (config.propositional['implication'],      lambda scanner,      _: tokens.BinaryOperator(BinaryOperators.implication)),
        (config.propositional['bi-implication'],   lambda scanner,      _: tokens.BinaryOperator(BinaryOperators.biimplication)),
        (config.propositional['negation'],         lambda scanner,      _: tokens.Negation()),
        (r"\s+", None), # None == skip token.
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
    # TODO raise error if remainder is not empty
    return results

if __name__ == "__main__":
    input_formula = "~a | c & q"
    logic = "KM"
    tokens = tokenize(logic, input_formula)
    print tokens