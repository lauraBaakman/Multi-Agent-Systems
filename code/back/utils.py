# -*- coding: utf-8 -*-

import json

"""."""

__author__ = 'laura'

class Stack(object):
    """
    Stack
    """

    def __init__(self):
        """
        Constructor for the stack
        """
        self.list = []


    def push(self, element):
        """
        Push an element on the stack
        :param element: the element to push
        :return: nothing
        """
        self.list.append(element)

    def pop(self):
        """
        Return the top element of the stack after it has been removed.
        :return: the first element on the stack, None if the stack is empty
        """
        return self.list.pop()

    def top(self):
        """
        Return the top element of the stack but don't remove it.
        :return: the first element on the stack, None if the stack is empty
        """
        return self.list[-1]

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

def read_json(filename):
    json_data = open(filename)
    data = json.load(json_data, object_hook=_decode_dict)
    json_data.close()
    return data