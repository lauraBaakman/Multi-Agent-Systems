# -*- coding: utf-8 -*-

__author__ = 'laura'


class Node(object):
    """General node class"""


def models(state, formula, delimiter=''):
    return "{delimiter}\left(M, \\text{{{state}}} \\right) \models {formula}{delimiter}".format(
        state=state.name,
        formula=formula.to_latex(),
        delimiter=delimiter
    )