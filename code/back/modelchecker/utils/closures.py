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

def convergence(set_a, set_b):
    return set_a == set_b

def transitive(original):
    """
    Compute the transitive closure of the original set.
    :param original: the set of which the transitive closure should be computed.
    :type original: set
    :return: the transitive closure of the original set
    :rtype: set
    """
    closure = original
    previous_set  = set()
    while not convergence(closure, previous_set):
        previous_set = closure
        new_relations = set((x, w) for x, y in closure for q, w in closure if q == y)
        closure = previous_set.union(new_relations)
    return closure

def symmetric(original):
    new_relations = [(destination, source) for (source, destination) in original]
    return original.union(new_relations)

def transitive_symmetric(original):
    """
    Compute the transitive symmetric closure
    :param original: the set of which the transitive symmetric closure should be computed.
    :type original: set
    :return: the transitive symmetric closure of set
    :rtype: set
    """
    closure = original
    previous_set = set()
    while not convergence(closure, previous_set):
        previous_set = closure
        new_relations = transitive(closure) | (symmetric(closure))
        closure = previous_set.union(new_relations)
    return closure