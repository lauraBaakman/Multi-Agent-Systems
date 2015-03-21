# -*- coding: utf-8 -*-

"""Enums representing the operators"""
from enum import Enum

__author__ = 'laura'


class Operator(Enum):
    pass

class Binary(Operator):
    conjunction = 1
    disjunction  = 2
    implication = 3
    biimplication = 4

    def to_latex(self):
        operator_to_latex = {
            Binary.conjunction : '\\land',
            Binary.disjunction : '\\lor',
            Binary.implication : '\\to',
            Binary.biimplication : '\\leftrightarrow'
        }
        return operator_to_latex.get(self)

class Unary(Operator):
    negation = 5
    common = 6
    # TODO everybody operator implementeren!!!!
    everybody = 7

    def to_latex(self):
        operator_to_latex = {
            Unary.negation: '\\lnot',
            Unary.common: '\\text{C}\\:',
            Unary.everybody: '\\text{E}\\:'
        }
        return operator_to_latex.get(self)


class Agent(Operator):
    knowledge = 8
    possible = 9

    def to_latex(self):
        operator_to_latex = {
            Agent.knowledge: '\\text{K}',
            Agent.possible: '\\text{M}\\:'
        }
        return operator_to_latex.get(self)