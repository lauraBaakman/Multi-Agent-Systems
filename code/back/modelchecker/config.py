# -*- coding: utf-8 -*-
"""
Configuration for the tokenizer
"""
__author__ = 'laura'

# The regular expressions for the different operators.
propositional = {
    'negation': r"~",
    'disjunction': r"[|]",
    'conjunction': r"&",
    'implication': r"->",
    'bi-implication': r"<->"
}

agent = {
    'knowledge': r"K_[1-9]+",
    'possible': r"M_[1-9]+"
}

group = {
    'common': r"C",
    'everybody': r"E",
    'implicit': r"I"
}

# The supported logics:
logics = ['KM', 'T', 'S4', 'S5', 'KEC', 'TEC', 'S4EC', 'S5EC', 'KI', 'TI', 'S4I', 'S5I']


