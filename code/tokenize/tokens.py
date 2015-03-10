# -*- coding: utf-8 -*-

"""
The definitions of the tokens
"""
__author__ = 'laura'


class Knows(object):
    """Token representing the knows operator (K)"""

    def __init__(self, agent):
        self.agent = agent

    def __repr__(self):
        """Print-friendly representation of the Knows object."""
        return (
            "K_{obj.agent}".format(obj=self)
        )