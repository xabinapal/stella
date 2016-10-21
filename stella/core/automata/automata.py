# -*- coding: utf-8 -*-

from stella.core.patterns import Singleton

__all__ = ['AutomatonState', 'TransitionTable', 'EpsilonTransition']

################################################################################
### AutomatonError
################################################################################

class AutomatonError(Exception):
    pass

################################################################################
### AutomatonState
################################################################################

class AutomatonState(object):
    def __init__(self, name, accepting=False):
        self.name = name
        self.accepting = accepting

################################################################################
### EpsilonTransition
################################################################################

class EpsilonTransition(metaclass=Singleton):
    pass

################################################################################
### TransitionTable
################################################################################

class TransitionTable(object):
    def __init__(self, non_deterministic=False):
        self.non_deterministic = non_deterministic
        self.table = {}

    def add(self, initial_state, final_state, symbol):
        if not self.non_deterministic and (
                symbol == EpsilonTransition or (
                    initial_state in self.table and
                    symbol in self.table[initial_state])):
            raise AutomatonError()

        if initial_state not in self.table:
            self.table[initial_state] = {}

        if symbol not in self.table[initial_state]:
            self.table[initial_state][symbol] = []

        self.table[initial_state][symbol].append(final_state)

    def get_transition(self, initial_state, symbol):
        if not self.non_deterministic and symbol == EpsilonTransition:
            raise AutomatonError()

        if initial_state not in self.table:
            return None

        if symbol not in self.table[initial_state]:
            return None

        return self.table[initial_state][symbol]
