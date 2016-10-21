from stella.core.automata import TransitionTable, AutomatonState

class NFA(object):
    def __init__(self, states=[], transitions=TransitionTable(True)):
        self.states = states
        self.state_count = len(states)
        self.transitions = transitions

    def add_state(self, name, accepting=False):
        state = AutomatonState(name, accepting)
        self.states.append(state)
        self.state_count += 1
        return state

    def add_transition(self, initial_state, final_state, value):
        self.transitions.add(initial_state, final_state, value)
