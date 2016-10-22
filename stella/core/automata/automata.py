# -*- coding: utf-8 -*-

from stella.core.patterns import Singleton

__all__ = ['AutomatonError', 'AutomatonState', 'TransitionTable', 'EpsilonTransition']

################################################################################
### AutomatonError
################################################################################

class AutomatonError(Exception):
    pass

################################################################################
### AutomatonState
################################################################################

class AutomatonState(object):
    def __init__(self, name, initial=False, accepting=False):
        self.name = name
        self.initial = initial
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
    def __init__(self, non_deterministic=False, symbol_checker=None):
        self.non_deterministic = non_deterministic
        self.table = {}

        if not symbol_checker:
            self.symbol_checker = self.__class__._symbol_checker
        else:
            self.symbol_checker = symbol_checker

    @staticmethod
    def _symbol_checker(symbol_table, symbol):
        if symbol not in symbol_table:
            return []

        return symbol_table[symbol]

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

    def get_transitions(self, state, symbol):
        if not self.non_deterministic and symbol == EpsilonTransition:
            raise AutomatonError()

        if state.name not in self.table:
            return []

        return self.symbol_checker(self.table[state.name], symbol)
