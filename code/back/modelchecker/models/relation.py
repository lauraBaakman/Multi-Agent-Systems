# -*- coding: utf-8 -*-

__author__ = 'laura'

class Relation(object):
    """
    Represents relations in a Kripke

    Attributes:
        - agent: The agent of the relation as a string.
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
        return "{obj.source.name}{obj.agent}{obj.destination.name}".format(obj=self)

    def __eq__(self, other):
        """Compare self with other."""
        return self.__dict__ == other.__dict__

    def to_tuple(self):
        return (self.source, self.destination, self.agent)

    def to_json_dump(self):
        """
        Return the object as the format required by to_json.
        :return:
        """
        return [self.source.name, self.agent, self.destination.name]

    def symmetric_relation(self):
        return Relation(
            self.agent,
            self.destination,
            self.source
        )

    @staticmethod
    def from_tuple((source, destination, agent)):
        return Relation(
            agent,
            source,
            destination
        )