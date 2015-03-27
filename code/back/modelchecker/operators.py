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


class Unary(Operator):
    negation = 5
    common = 6
    everybody = 7


class Agent(Operator):
    knowledge = 8
    possible = 9