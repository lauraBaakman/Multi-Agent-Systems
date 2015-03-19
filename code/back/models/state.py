# -*- coding: utf-8 -*-

import kmmodel

__author__ = 'laura'


class State(object):
    """
    State object

    Attributes:
        - incoming: dictionary of incoming relations, indexed by agent.
        - outgoing: dictionary of outgoing relations, indexed by agent.
        - valuations: dictionary of valuations, indexed by proposition.
    """

    def __init__(self, name, valuations):
        """
        Constructor for State object
        :param valuations: dictionary with the propositions and their valuations.
        :param name: name of the state
        """
        self.name = name
        self.incoming = {}
        self.outgoing = {}
        self.valuations = valuations

    def _add_relation(self, dictionary, relation):
        relations = dictionary.get(relation.agent)
        if relations:
            relations.append(relation)
        else:
            dictionary[relation.agent] = [relation]

    def add_outgoing_relation(self, relation):
        """
        Add outgoing relation to the state, do nothing if the relation already exists.
        :param relation: the relation
        :return: void
        """
        self._add_relation(self.outgoing, relation)

    def add_incoming_relation(self, relation):
        """
        Add incoming relation to the state, do nothing if the relation already exists.
        :rtype : None
        :param relation: the relation
        :return: void
        """
        self._add_relation(self.incoming, relation)

    def __repr__(self):
        return (
            "{obj.name} [in: {obj.incoming}, out: {obj.outgoing}, valuations: {obj.valuations}]\n"
            .format(
                obj=self,
            )
        )

    def __eq__(self, other):
        """Compare self with other."""
        return self.__dict__ == other.__dict__

    def to_json_dump(self):
        return {
            'id' : self.name,
            'vals': self.valuations.values()
        }
