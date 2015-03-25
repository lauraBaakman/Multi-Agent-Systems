# -*- coding: utf-8 -*-
from unittest import TestCase

import modelchecker.utils as utils
import modelchecker.models as models

__author__ = 'laura'



class TestTModel(TestCase):
    def test_reflexive_closure(self):
        filename = './modelchecker/models/test_model_t.json'
        data = utils.read_json(filename)
        model = models.TModel.from_json(data)
        self.assertIs(len(model.relations.get('1')), 3)
        self.assertIs(len(model.relations.get('2')), 2)
        print model