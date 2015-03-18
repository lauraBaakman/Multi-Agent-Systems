# -*- coding: utf-8 -*-

__author__ = 'laura'

import state

class Relation(object):
    """
    Represents relations in a Kripke Model

    Attributes:
        - agent: The agent of the relation
        - source: The source of the relation:
        - destination: The destination of the relation.
    """

    def __init__(self, agent, source, destination):
        """
        Constructor
        :param agent: the name of the agent
        :param source: the source state
        :param destination: the destination state
        :return:
        """
        self.agent = agent
        self.source = source
        self.destination = destination

    def __repr__(self):
        """Print friendly representation."""
        return "{obj.source}{obj.agent}{obj.destination}".format(obj=self)

    def __eq__(self, other):
        """Compare self with other."""
        return self.__dict__ == other.__dict__