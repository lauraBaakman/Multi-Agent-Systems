# -*- coding: utf-8 -*-

__author__ = 'laura'

def reflexive(original, states):
    """
    Compute the reflexive closure of the original set.
    :param original: the set of which the reflexive closure should be computed.
    :type original: set
    :param states: list of elements to avoid
    :type states: list
    :return: the reflexive closure of original set.
    :rtype: set
    """
    reflexive_relations = [(state, state) for state in states]
    return original.union(reflexive_relations)
