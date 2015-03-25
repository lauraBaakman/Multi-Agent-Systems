# -*- coding: utf-8 -*-

from modelchecker import errors

__author__ = 'laura'


class State(object):
    """
    State object

    Attributes:
        - incoming: dictionary of incoming relations, indexed by agent as string.
        - outgoing: dictionary of outgoing relations, indexed by agent as string.
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
            if not(relation in relations):
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

    def is_true(self, proposition):
        """
        Returns the truth value of the proposition
        :param proposition: the proposition
        :return: the truth value of the proposition
        """
        result = self.valuations.get(
            proposition,
            errors.ValuationError(
                "The proposition '{proposition}' does not have a valuation in state '{state_name}'"
                .format(
                    proposition=proposition,
                    state_name=self.name
                )
            ),
        )
        if isinstance(result, errors.ValuationError):
            raise result
        return result


    def __repr__(self):
        return (
            "{obj.name} [in: {obj.incoming}, out: {obj.outgoing}, valuations: {obj.valuations}]\n"
            .format(
                obj=self,
            )
        )

    def __eq__(self, other):
        """Compare self with other."""
        return self.name == other.name

    def to_json_dump(self):
        return {
            'id' : self.name,
            'vals': self.valuations.values()
        }
