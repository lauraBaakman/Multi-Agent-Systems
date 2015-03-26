# -*- coding: utf-8 -*-
from unittest import TestCase

from closures import  *

__author__ = 'laura'


class TestReflexive(TestCase):

    def test_reflexive(self):
        states = [1, 2, 3, 4]
        original_set = set([(1, 2), (2,3)])
        expected_result = original_set.union([(1,1), (2,2), (3,3), (4,4)])
        computed_result = reflexive(original_set, states)
        self.assertEquals(expected_result, computed_result)

class TestTransitive(TestCase):
    def test_transitive(self):
        original_set = set([(1, 2), (2, 3), (3, 4)])
        expected_result = original_set.union([(1,3), (1,4), (2, 4)])
        computed_result = transitive(original_set)
        self.assertEquals(expected_result, computed_result)

class TestSymmetric(TestCase):
    def test_symmetric(self):
        original_set = set([(1, 2), (2, 3), (3, 4)])
        expected_result = original_set.union([(2, 1), (3, 2), (4, 3)])
        computed_result = symmetric(original_set)
        self.assertEquals(expected_result, computed_result)

class TestTransitiveSymmetric(TestCase):
    def test_transitive_symmetric(self):
        original_set = set([(1, 2), (2, 3), (3, 4)])
        expected_result = original_set.union([
            (1,3), (1,4), (2,4),
            (2, 1), (3, 2), (4, 3),
            (4,2), (4,1), (3,1),
            (1, 1), (2, 2), (3, 3), (4,4)
        ])
        computed_result = transitive_symmetric(original_set)
        self.assertEquals(expected_result, computed_result)