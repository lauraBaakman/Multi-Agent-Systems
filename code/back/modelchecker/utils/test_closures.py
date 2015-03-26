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