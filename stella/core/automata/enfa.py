# -*- coding: utf-8 -*-

from stella.core.automata import *

import itertools

__all__ = ['ENFA']

class ENFA(object):
    def __init__(self, states=None, transitions=None, symbol_checker=None):
        if states == None:
            self.states = []
        else:
            self.states = states
    
        if transitions == None:
            self.transitions = TransitionTable(
                non_deterministic=True,
                symbol_checker=symbol_checker)
        else:
            self.transitions = transitions
            if symbol_checker:
                self.transitions.symbol_checker = symbol_checker

        self.reset()
        
    def add_state(self, name, initial=False, accepting=False):
        if initial:
            if next((x for x in self.states if x.initial), None):
                raise AutomatonError()

        state = AutomatonState(name, initial, accepting)
        self.states.append(state)
        self.state_count += 1
        if initial:
            self.initial_state = state

        return state

    def add_transition(self, initial_state, final_state, value):
        self.transitions.add(initial_state, final_state, value)

    def compile(self):
        count = 0
        if not self.initial_state:
            return

        self.current_states.add(self.initial_state)
        while count != len(self.current_states):
            count = len(self.current_states)
            t = self._get_epsilon_transitions(self.current_states)
            self.current_states.update(t)

    def reset(self):
        self.initial_state = next((x for x in self.states if x.initial), None)
        self.state_count = len(self.states)
        self.current_states = set()
        self.input_symbols = []
        self.compile()

    def input(self, symbol):
        next_states = self.get_next_states(symbol)
        self.current_states = next_states
        self.input_symbols.append(symbol)

    def get_next_states(self, symbol):
        next_states = set()
        if self.current_states:
            for x in self.current_states:
                t = self.transitions.get_transitions(x, symbol)
                t = [x for x in self.states if x.name in t]
                next_states.update(t)

            t = self._get_epsilon_transitions(next_states)
            next_states.update(t)

        next_states.update(self._get_epsilon_transitions(next_states))

        return next_states

    def next_is_valid_state(self, symbol):
        next_states = self.get_next_states(symbol)
        return len(next_states) != 0

    @property
    def valid_state(self):
        return len(self.current_states) != 0

    @property
    def accepting_state(self):
        return any(x.accepting for x in self.current_states)

    @property
    def current_transitions(self):
        states = set(self.current_states)
        states.update(self._get_epsilon_transitions(states))

        transitions = set()
        for x in self.current_states:
            t = self.transitions.get_state_transitions(x)
            transitions.update(t)

        return transitions
        
    def _get_epsilon_transitions(self, states):
        t = (self.transitions.get_transitions(x, Epsilon) for x in states)
        t = set(itertools.chain.from_iterable(t))
        transitions = set(x for x in self.states if x.name in t)

        count = 0
        while count != len(transitions):
            count = len(transitions)
            t = (self.transitions.get_transitions(x, Epsilon) for x in transitions)
            t = set(itertools.chain.from_iterable(t))
            transitions.update(x for x in self.states if x.name in t)

        return transitions
