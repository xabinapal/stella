# -*- coding: utf-8 -*-

from stella.core.automata import *

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
            t = self._get_epsilon_transitions()
            self.current_states.update(t)

    def reset(self):
        self.initial_state = next((x for x in self.states if x.initial), None)
        self.state_count = len(self.states)
        self.current_states = set()
        self.input_symbols = []
        self.compile()

    def input(self, symbol):
        if not self.current_states and self.input_symbols:
            return

        next_states = set()
        for x in self.current_states:
            t = self.transitions.get_transitions(x, symbol)
            t = [x for x in self.states if x.name in t]
            if t:
                next_states.update(t)

        self.current_states = next_states
        self.input_symbols.append(symbol)
        t = self._get_epsilon_transitions()
        self.current_states.update(t)

    def valid_state(self):
        return len(self.current_states) != 0

    def accepting_state(self):
        return any(x.accepting for x in self.current_states)

    def current_transitions(self):
        transitions = set()
        for x in self.current_states:
            t = self.transitions.get_state_transitions(x)
            transitions.update(t)

        return transitions
        
    def _get_epsilon_transitions(self):
        transitions = set()
        for x in self.current_states:
            t = self.transitions.get_transitions(x, Epsilon)
            t = [x for x in self.states if x.name in t]
            if t:
                transitions.update(t)

        return transitions
