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

def transitive(original):
    """
    Compute the transitive closure of the original set.
    :param original: the set of which the transitive closure should be computed.
    :type original: set
    :return: the transitive closure of the original set
    :rtype: set
    """
    closure = original
    while True:
        new_relations = set((x, w) for x, y in closure for q, w in closure if q == y)
        closure_until_now = closure | new_relations
        if closure_until_now == closure:
            break
        closure = closure_until_now
    return closure