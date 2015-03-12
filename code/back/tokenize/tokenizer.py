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
    km_s5_expressions = []

    s5EC_expressions = []

    expressions_per_logic = {
        "KM": km_s5_expressions,
        "S5": km_s5_expressions,
        "S5EC": s5EC_expressions
    }

    regular_expressions = []

    regular_expressions.append(expressions_per_logic.get(logic, []))
    return regular_expressions

def tokenize(logic, string):
    """
    Tokenize the inputted string to a list of tokens
    :param loigc: The logic of the string, options: KM, S5, S5EC
    :param string: The string to be tokenized
    :return:[object]
    """
    regular_expressions = regular_expressions(logic);


if __name__ == "__main__":
    input_formula = "~a | C & q"

    scan = re.Scanner([
        (r"[a-z]\w*",                              lambda scanner,  token: tokens.Proposition(token)),
        (config.propositional['conjunction'],      lambda scanner,      _: tokens.BinaryOperator(BinaryOperators.conjunction)),
        (config.propositional['disjunction'],      lambda scanner,      _: tokens.BinaryOperator(BinaryOperators.disjunction)),
        (config.propositional['implication'],      lambda scanner,      _: tokens.BinaryOperator(BinaryOperators.implication)),
        (config.propositional['bi-implication'],   lambda scanner,      _: tokens.BinaryOperator(BinaryOperators.biimplication)),
        (config.propositional['negation'],         lambda scanner,      _: tokens.Negation()),
        (r"\s+", None), # None == skip token.
    ])
    results, remainder=scan.scan(input_formula)
    print results
    print remainder