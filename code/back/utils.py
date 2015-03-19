# -*- coding: utf-8 -*-

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
