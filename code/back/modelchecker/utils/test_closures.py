# -*- coding: utf-8 -*-
from unittest import TestCase

from closures import  *

__author__ = 'laura'


class TestReflexive(TestCase):

    def test_reflexive(self):
        states = [1, 2, 3, 4]
        original_set = set([(1, 2), (2,3)])
        expected_result = set([(1,1), (2,2), (3,3), (4,4), (1,2), (2,3)])
        computed_result = reflexive(original_set, states)
        self.assertEquals(expected_result, computed_result)