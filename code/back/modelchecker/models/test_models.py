# -*- coding: utf-8 -*-
from unittest import TestCase

import modelchecker.utils as utils
import modelchecker.models as models

__author__ = 'laura'



class TestModel(TestCase):
    # def test_reflexive_closure(self):
    #     filename = './modelchecker/models/test_model_t.json'
    #     data = utils.read_json(filename)
    #     model = models.TModel.from_json(data)
    #     self.assertIs(len(model.relations.get('1')), 3)
    #     self.assertIs(len(model.relations.get('2')), 2)

    # def test_transitive_closure(self):
    #     filename = './modelchecker/models/test_model_s4.json'
    #     data = utils.read_json(filename)
    #     model = models.S4Model.from_json(data)
    #     print model


    def test_symmetric_closure(self):
        filename = './modelchecker/models/test_model_s5.json'
        data = utils.read_json(filename)
        model = models.S5Model.from_json(data)
        print model


