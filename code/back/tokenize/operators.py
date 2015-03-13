# -*- coding: utf-8 -*-

"""Enums representing the operators"""
from enum import Enum

__author__ = 'laura'


class Binary(Enum):
    conjunction = 1
    disjunction  = 2
    implication = 3
    biimplication = 4


class Unary(Enum):
    negation = 1
    common = 2


class Modal(Enum):
    knowledge = 1
    possible = 2